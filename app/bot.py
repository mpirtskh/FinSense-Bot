from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.llm import create_llm
from app.tools import (
    get_time, get_date, get_weather_info, 
    get_currency_rates, convert_money, 
    search_banking_help, get_banking_overview
)
from app.config import get_system_prompt

class TBCBot:
    def __init__(self):
        self.llm = create_llm()
        self.tools = [
            get_time, get_date, get_weather_info,
            get_currency_rates, convert_money,
            search_banking_help, get_banking_overview
        ]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.conversation_history = [SystemMessage(content=get_system_prompt())]
    
    def chat(self, user_message):
        """Process a user message and return a response."""
        self.conversation_history.append(HumanMessage(content=user_message))
        
        response = self.llm_with_tools.invoke(self.conversation_history)
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            tool_results = []
            for tool_call in response.tool_calls:
                tool_name = tool_call.get('name')
                tool_args = tool_call.get('args', {})
                
                tool_func = next((t for t in self.tools if t.name == tool_name), None)
                if tool_func:
                    try:
                        result = tool_func.invoke(tool_args)
                        tool_results.append(f"Tool result: {result}")
                    except Exception as e:
                        tool_results.append(f"Tool error: {str(e)}")
            
            if tool_results:
                tool_response = "\n".join(tool_results)
                self.conversation_history.append(AIMessage(content=tool_response))
                
                final_response = self.llm.invoke(self.conversation_history)
                self.conversation_history.append(final_response)
                return final_response.content
        
        self.conversation_history.append(response)
        return response.content
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = [SystemMessage(content=get_system_prompt())]