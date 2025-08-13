from __future__ import annotations

from typing import Dict, Optional, List

BANKING_FAQS = {
    "greetings": {
        "question": "hello",
        "answer": "გამარჯობა! მე ვარ TBC ბანკის AI ასისტენტი. როგორ შემიძლია დაგეხმაროთ ? (Hello! I'm TBC Bank's AI assistant. How can I help you today?)"
    },
    "greetings_hi": {
        "question": "hi",
        "answer": "გამარჯობა! მოგესალმებთ TBC ბანკის ვირტუალური ასისტენტი. რით შემიძკუა დაგეხმაროთ? "
    },
    "greetings_gamarjoba": {
        "question": "გამარჯობა",
        "answer": "გამარჯობა! მე ვარ TBC ბანკის AI ასისტენტი. შემიძლია დაგეხმაროთ საბანკო საკითხებში, სავალუტო კურსებში,  მოგაწოდოთ ინფორმაცია ამინდსა და დროზე. (Hello! I'm TBC Bank's AI assistant. I can help you with banking questions, exchange rates, weather, or time.)"
    },
    "account_types": {
        "question": "რა ტიპის ანგარიშები გაქვთ?",
        "answer": "TBC ბანკში შეგიძლიათ გახსნათ: 1) მიმდინარე ანგარიში (სახელფასო), 2) დანაზოგი ანგარიში, 3) ვალუტის ანგარიში (USD, EUR), 4) ბიზნეს ანგარიში. ყველა ანგარიში შეგიძლიათ გახსნათ ონლაინ ან ფილიალში."
    },
    "card_fees": {
        "question": "რა საკომისიოები არის ბარათებზე?",
        "answer": "TBC ბარათების საკომისიოები: 1) ყოველწლიური მომსახურება - 15-25 GEL (ბარათის ტიპის მიხედვით), 2) ფულის გამოტანა ATM-დან - 1-2 GEL, 3) უცხოურ ბანკში გამოყენება - 2-3% + საკომისიო. ზოგიერთი პრემიუმ ბარათი უფასოა."
    },
    "transfer_limits": {
        "question": "რა ლიმიტები არის გადარიცხვებზე?",
        "answer": "TBC გადარიცხვების ლიმიტები: 1) ყოველდღიური - 50,000 GEL (სტანდარტული), 2) ყოველთვიური - 500,000 GEL, 3) საერთაშორისო - 25,000 USD ეკვივალენტი დღეში. ლიმიტების გაზრდა შეგიძლიათ ბანკში მიმართოთ."
    },
    "loan_requirements": {
        "question": "რა დოკუმენტები სჭირდება სესხის მისაღებად?",
        "answer": "TBC სესხისთვის საჭიროა: 1) პასპორტი/ID ბარათი, 2) სახელფასო ცნობა ან 6 თვის ბანკის ანგარიშის ისტორია, 3) სამუშაო ცნობა, 4) ქონების დოკუმენტები (თუ სჭირდება). პირველი სესხი 3-6 თვის სამუშაო გამოცდილებას მოითხოვს."
    },
    "security_tips": {
        "question": "როგორ დავიცავ ბანკის ანგარიშს?",
        "answer": "TBC უსაფრთხოების რჩევები: 1) არ გაუზიაროთ PIN კოდი ან SMS კოდი, 2) ყოველთვის გამოიყენეთ ოფიციალური TBC ბანკის აპი, 3) არ დააჭიროთ უცნობი ლინკები, 4) ჩართეთ SMS ნოტიფიკაციები, 5) რეგულარულად შეცვალეთ პაროლები."
    },
    "online_banking": {
        "question": "როგორ გავხსნა ონლაინ აგარიში?",
        "answer": "TBC ონლაინ ბანკინგის გასახსნელად: 1) გადადით tbcbank.ge-ზე, 2) დააჭირეთ 'შესვლა' და 'რეგისტრაცია', 3) შეიყვანეთ პირადი ნომერი და ბარათის ნომერი, 4) მიიღეთ SMS კოდი და შეიყვანეთ, 5) დააყენეთ პაროლი. პირველად ფილიალში უნდა გადახვიდეთ ვერიფიკაციისთვის."
    }
}

def search_banking_faq(query: str) -> Optional[Dict[str, str]]:
    # simple search function for banking FAQ
    query_lower = query.lower().strip()
    
    # Check for exact matches first (for greetings)
    for key, faq in BANKING_FAQS.items():
        if query_lower == faq["question"].lower():
            return faq
    
    best_match = None
    best_score = 0
    
    for key, faq in BANKING_FAQS.items():
        score = 0
        
        # check question words
        question_words = faq["question"].lower().split()
        for word in query_lower.split():
            if word in question_words:
                score += 2
        
        # check answer words
        answer_words = faq["answer"].lower().split()
        for word in query_lower.split():
            if word in answer_words:
                score += 1
        
        # special keywords get bonus points
        if "საკომისიო" in query_lower or "fee" in query_lower:
            if "card_fees" in key:
                score += 5
        
        if "ანგარიში" in query_lower or "account" in query_lower:
            if "account_types" in key:
                score += 5
        
        if "სესხ" in query_lower or "loan" in query_lower:
            if "loan_requirements" in key:
                score += 5
        
        if "უსაფრთხოებ" in query_lower or "security" in query_lower:
            if "security_tips" in key:
                score += 5
        
        if "ონლაინ" in query_lower or "online" in query_lower:
            if "online_banking" in key:
                score += 5
        
        # update best match
        if score > best_score:
            best_score = score
            best_match = faq
    
    return best_match if best_score > 0 else None

def get_all_faqs() -> List[Dict[str, str]]:
    return list(BANKING_FAQS.values())
