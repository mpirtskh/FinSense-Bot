from __future__ import annotations

import json
from typing import Annotated, Dict, List, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, SystemMessage, ToolMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from .llm import create_llm
from .config import get_system_prompt, get_openai_model
from .nodes.tools import (
    tool_get_time, 
    tool_get_weather, 
    tool_search_banking_faq, 
    tool_get_exchange_rates, 
    tool_convert_currency
)
from .services.usage_tracker import usage_tracker


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]


def build_graph() -> StateGraph:
    # get the system prompt for the bot
    system_prompt = get_system_prompt()
    
    # create the language model with tools
    llm = create_llm().bind_tools([
        tool_get_time,
        tool_get_weather,
        tool_search_banking_faq, 
        tool_get_exchange_rates, 
        tool_convert_currency
    ])

    # make a dictionary to look up tools by name
    tools_by_name = {}
    tools_by_name[tool_get_time.name], tools_by_name[tool_get_weather.name], tools_by_name[tool_search_banking_faq.name], tools_by_name[tool_get_exchange_rates.name], tools_by_name[tool_convert_currency.name] = tool_get_time, tool_get_weather ,tool_search_banking_faq, tool_get_exchange_rates, tool_convert_currency
    

    def agent_node(state: AgentState) -> Dict[str, List[BaseMessage]]:
        # get messages from state
        messages = state.get("messages", [])
        
        # add system prompt if not there
        has_system = False
        for m in messages:
            if isinstance(m, SystemMessage):
                has_system = True
                break
        
        if not has_system:
            messages = [SystemMessage(content=system_prompt)] + messages
        
        # get response from AI
        response = llm.invoke(messages)
        
        # track usage (simple way)
        try:
            input_len = sum(len(str(m.content)) for m in messages)
            output_len = len(response.content) if hasattr(response, 'content') else 0
            usage_tracker.log_call(
                model=get_openai_model(),
                input_tokens=input_len // 4,
                output_tokens=output_len // 4
            )
        except:
            pass  # ignore errors in usage tracking
        
        return {"messages": [response]}

    def should_continue(state: AgentState) -> str:
        # check if we need to call tools
        last_message = state["messages"][-1]
        if isinstance(last_message, AIMessage):
            if hasattr(last_message, "tool_calls"):
                if last_message.tool_calls:
                    return "call_tools"
        return "end"

    def call_tools(state: AgentState) -> Dict[str, List[ToolMessage]]:
        # execute tools that AI wants to use
        last_message = state["messages"][-1]
        tool_messages = []
        
        for tool_call in last_message.tool_calls:
            # get tool info
            tool_name = tool_call.get("name")
            tool_args = tool_call.get("args", {})
            call_id = tool_call.get("id")
            
            # find the tool
            tool = tools_by_name.get(tool_name)
            
            if tool is None:
                content = f"Tool {tool_name} not found"
            else:
                try:
                    # run the tool
                    result = tool.invoke(tool_args)
                    if isinstance(result, str):
                        content = result
                    else:
                        content = json.dumps(result)
                except Exception as e:
                    content = f"Error running tool {tool_name}: {e}"
            
            # create message
            tool_message = ToolMessage(content=content, tool_call_id=call_id)
            tool_messages.append(tool_message)
        
        return {"messages": tool_messages}

    # build the workflow
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("call_tools", call_tools)
    workflow.set_entry_point("agent")
    
    # add the routing logic
    workflow.add_conditional_edges(
        "agent", 
        should_continue, 
        {"call_tools": "call_tools", "end": END}
    )
    workflow.add_edge("call_tools", "agent")
    
    return workflow