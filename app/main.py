from __future__ import annotations

from typing import List, Optional, Dict

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from rich.console import Console
from rich.markdown import Markdown

from .graph import build_graph
from .config import get_system_prompt

def main_loop() -> None:
    console = Console()
    
    # build the bot
    app = build_graph().compile()

    system_prompt = get_system_prompt()
    
    messages: List[BaseMessage] = [SystemMessage(content=system_prompt)]

    # welcome message
    console.print(Markdown("მოგესალმებათ **TBC ბოტი**. დაუსვით თქვენთვის სასურველი კითხვა და ეცდება თქვენს დახმარებას, ინტერაქციის დასასრულებლად კი მიწერეთ ბოტს \"ნახვამდის\" ან \"მადლობ\""))

    # banking flow state
    banking_flow = {
        "active": False,
        "step": 0,
        "account_type": "",
        "personal_info": {}
    }

    while True:
        try:
            # get user input
            user_input = console.input("[bold cyan]მომხმარებელი:[/bold cyan] ")
        except (EOFError, KeyboardInterrupt):
            console.print("\nნახვამდის! 👋")
            break

        greetings = ["hi", "გამარჯობა", "სალამი", "ჰაი", "gamarjoba", "hii", "salami"]
        if user_input.strip().lower() in greetings:
            console.print("[bold green]ბოტი:[/bold green]", "გამარჯობა!👋 მიხარია რომ მომწერე, რით შემიძლია შენი დახმარება?")
            continue

        # quit commands
        quit_words = {"exit", "ნახვამდის", "naxvamdis", "bye", "kargad", "მადლობ", "მადლობა", "წავედი", "კარგად"}
        if user_input.strip().lower() in quit_words:
            console.print("ნახვამდის! 👋")
            break

        # check for banking flow start
        if ("account" in user_input.lower() or "ანგარიში" in user_input.lower()) and ("დარეგისტრირება" in user_input.lower() or "შექმნა" in user_input.lower() or "გახსნა" in user_input.lower() ):
            banking_flow["active"] = True
            banking_flow["step"] = 1
            console.print("[bold green]ბოტი:[/bold green]", "მე დაგეხმარებით ანგარიშის გახსნაში. რა ტიპის ანგარიშის გახსნა გინდათ?")
            console.print("გთხოვთ მოიწეროთ რიცხვი ან სიტყვიერად")
            console.print("1. სახელფასო ანგარიში")
            console.print("2. ბიზნესის ანგარიში")
            console.print("3. მულტისავალუტო ანგარიში")
            continue

        # handle banking flow steps
        if banking_flow["active"]:
            response = handle_banking_flow(user_input, banking_flow, console)
            if response:
                console.print("[bold green]ბოტი:[/bold green]", response)
            continue

        messages.append(HumanMessage(content=user_input))
        
        state = {"messages": messages}
        
        # get bot response
        result = app.invoke(state)
        messages = result["messages"]

        # show AI response
        ai_messages = []
        for m in messages:
            if isinstance(m, AIMessage):
                ai_messages.append(m)
        
        if ai_messages:
            console.print("[bold green]ბოტი:[/bold green]", ai_messages[-1].content)


def handle_banking_flow(user_input: str, banking_flow: Dict, console: Console) -> Optional[str]:
    """Handle the multi-step banking flow for account opening."""
    
    if banking_flow["step"] == 1:
        # Step 1: Account type selection
        user_input_clean = user_input.strip().lower()
        

        if user_input_clean in ["1", "2", "3"]:
            account_types = {
                "1": "სახელფასო ანგარიში",
                "2": "ბიზნეს ანგარიში", 
                "3": "სავალუტო ანგარიში (USD, EUR)",
            }
            banking_flow["account_type"] = account_types[user_input_clean]
            banking_flow["step"] = 2
            
            return f"აირჩიეთ {banking_flow['account_type']}. ახლა მითხარით თქვენი სახელი და გვარი:"
        
        #  text alternatives
        elif any(word in user_input_clean for word in ["სახელფასო", "salary", "salary", "1"]):
            banking_flow["account_type"] = "სახელფასო ანგარიში"
            banking_flow["step"] = 2
            return f" {banking_flow['account_type']}-ის გახსნისთვის გთხოვთ შეიყვანოთ სახელი და გვარი:"
        
        elif any(word in user_input_clean for word in ["ბიზნეს", "business", "biznes", "2"]):
            banking_flow["account_type"] = "ბიზნეს ანგარიში"
            banking_flow["step"] = 2
            return f" {banking_flow['account_type']}-ის გახსნისთვის გთხოვთ შეიყვანოთ სახელი და გვარი:"
        
        elif any(word in user_input_clean for word in ["სავალუტო", "currency", "valuta", "usd", "eur", "3"]):
            banking_flow["account_type"] = "სავალუტო ანგარიში (USD, EUR)"
            banking_flow["step"] = 2
            return f" {banking_flow['account_type']}-ის გახსნისთვის გთხოვთ შეიყვანოთ სახელი და გვარი:"
        
        else:
            return "გთხოვთ აირჩიოთ 1, 2, ან 3, ან დაწერეთ ანგარიშის ტიპი (სახელფასო, ბიზნეს, სავალუტო):"
    
    elif banking_flow["step"] == 2:
        # Step 2: Personal information - more flexible
        user_input_clean = user_input.strip()
        
        # check if it looks like a name (2+ words, reasonable length)
        if len(user_input_clean.split()) >= 2 and len(user_input_clean) >= 4:
            banking_flow["personal_info"]["name"] = user_input_clean
            banking_flow["step"] = 3
            return "შეიყვანეთ პირადობის ნომერი"
        else:
            return "გთხოვთ შეიყვანოთ სრული სახელი და გვარი :"
    
    elif banking_flow["step"] == 3:
        # Step 3: ID number
        user_input_clean = user_input.strip()
        
        # რიცხვები არის თუ არა, ზედმეტი სიმბოლოები ჩავანაცვლოთ
        clean_id = user_input_clean.replace(" ", "").replace("-", "").replace("_", "")
        
        if len(clean_id) >= 9 and clean_id.isdigit():
            banking_flow["personal_info"]["id_number"] = clean_id
            banking_flow["step"] = 4
            return "შეიყვანეთ თქვენი ტელეფონის ნომერი:"
        else:
            return " არასწორია, გთხოვთ შეიყვანოთ სწორი პირადობის ნომერი (მინიმუმ 9 ციფრი):"
    
    elif banking_flow["step"] == 4:
        # ტელ ნომერი
        user_input_clean = user_input.strip()
        
        # ზედმეტი სიმბოლოები ჩავანაცვლოთ
        clean_phone = user_input_clean.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace("+", "")
        
        if len(clean_phone) >= 9 and clean_phone.isdigit():
            banking_flow["personal_info"]["phone"] = clean_phone
            banking_flow["step"] = 5
            
            # შეჯამება
            summary = f"""
            📋 ანგარიშის გახსნის შეჯამება:
            🏦 ანგარიშის ტიპი: {banking_flow['account_type']}
            👤 სახელი: {banking_flow['personal_info']['name']}
            🆔 ნომერი: {banking_flow['personal_info']['id_number']}
            📱 ტელეფონი: {banking_flow['personal_info']['phone']}

            გსურთ გააგრძელოთ? (მოიწერეთ "დიახ ან არა")
                        """
            return summary
        else:
            return "გთხოვთ შეიყვანოთ სწორი ტელეფონის ნომერი (მინიმუმ 9 ციფრი):"
    
    elif banking_flow["step"] == 5:
        # Confirmation
        user_input_clean = user_input.strip().lower()
        
        if user_input_clean in ["დიახ", "კი", "ხოოო", "yes", "ki", "qi", "ok", "კარგი", "y"]:
            banking_flow["step"] = 6
            return "მადლობ! 🎉 ჩვენი თანამშრომელი დაგიკავშირდებათ 24 საათის განმავლობაში დეტალების დასაზუსტებლად."
        elif user_input_clean in ["არა", "no", "ara", "n", "ნო"]:
            # Reset flow
            banking_flow["active"] = False
            banking_flow["step"] = 0
            banking_flow["account_type"] = ""
            banking_flow["personal_info"] = {}
            return "კარგი, ანგარიშის გახსნა შეჩერებულია."
        else:
            return "გთხოვთ უპასუხოთ 'დიახ' ან 'არა':"
    
    elif banking_flow["step"] == 6:
        # Flow complete, reset
        banking_flow["active"] = False
        banking_flow["step"] = 0
        banking_flow["account_type"] = ""
        banking_flow["personal_info"] = {}
        return "როგორ შემიძლია დაგეხმაროთ?"
    
    return None


if __name__ == "__main__":
    main_loop()
