# models/category.py

class Category:
    def __init__(self, name):
        self.name = name
        self.total_amount = 0 # Sum of all transactions in this category

    vendor_category_map = {
        "WHOLEFDS CAM 10010": "Groceries",
        "WHOLEFDS MDF 10380": "Groceries",
        "WHOLEFDS BVL #10618": "Groceries",
        "STOP & SHOP 0081": "Groceries",
        "K-2 MARKET": "Groceries",
        "MARKET BASKET 28": "Groceries",
        "TARGET 1001": "Groceries",
        "SAINSBURY S CAMBRIDGE": "Groceries",
        
        "HARVARD CONTINUING E": "Education",
        "OPENAI": "Education",

        "PROGRESSIVE INS": "Insurance",
        
        "PANINI PIZZA COMPANY": "Eating Out",
        "CHIPOTLE 1957": "Eating Out",
        "BREEZY HILL ORCHARD": "Eating Out",
        "HALVA KEBAB": "Eating Out",
        "FAR OUT ICE CREAM": "Eating Out",
        "SQ *MIKE & PATTY'S /": "Eating Out",
        "DUNKIN #302531": "Eating Out",
        "RINCON LIMENO RESTAU": "Eating Out",
        "CHA FEO": "Eating Out",
        "PY *THE HALAL GUYS": "Eating Out",
        "SAWASDEE RESTAURANT": "Eating Out",
        "SQ *DOWNRIVER ICE CR": "Eating Out",
        "MCDONALD'S F23421": "Eating Out",
        "CHIPOTLE ONLINE": "Eating Out",
        "UEP*DUMPLING BUDDY": "Eating Out",
        "SQ *KIOSK ON THE GREEN": "Eating Out",
        "OVESUVIO LTD": "Eating Out",
        "AZ RDC CATERING": "Eating Out",

        "ROCCOS SPORTS & REC": "Entertainment",
        "GOODREC.COM": "Entertainment",
        "SQ *617 SMOKE SHOP": "Entertainment",
        "TRUSTEES* TRUSTEES R": "Entertainment",
        "GORE MOUNTAIN WEB": "Entertainment",
        "SLIPPI LLC": "Entertainment",
        "Spotify USA": "Entertainment",

        "AUTOZONE #5003": "Car Supplies",
        "RMV E-SERVICES": "Car Supplies",
        
        "CVS/PHARMACY #00714": "House Supplies",

        "LYFT   *RIDE SAT 7PM": "Travel",
        "DELTA AIR LINE DL EV": "Travel",
        "MTA*NYCT PAYGO": "Travel",
        "NEW BRUNSWICK PARKIN": "Travel",
        "PMUSA 201010 BOSTON": "Travel",
        "City of Cambridge": "Travel",
        "BLUEBIK*1 RIDE": "Travel",
        "BLUEBIK*TEMP HOLD": "Travel",
        "HILTON HOTEL EAST BR": "Travel",
        "PARKMOBILE": "Travel",
        "Voi UK": "Travel",
        "COT*FLT": "Travel",
        "STAGECOACH": "Travel",
        "STEPHENSONS OF ESSEX": "Travel",

        "BUFFALO EXCHANGE NY0": "Clothes",
        "GARMENT ONE GAR": "Clothes",
        "Uniqlo USA LLC UNIQL": "Clothes",

        "DENVER PAY BY PHONE": "Misc.",
        
        }

    @classmethod
    def get_category_for_vendor(cls, vendor):
        """ 
        Returns the category for a given vendor based on the mapping.
        If no match is found, default sets to "Misc."
        """
        
        category = cls.vendor_category_map.get(vendor)
        valid_categories = set(cls.vendor_category_map.values())
        if not category:
            print(f"\nNo category found for vendor: '{vendor}'")
            print("Valid categories:", ", ".join(valid_categories))

            while True:
                user_input = input("Please enter a category for this vendor: ").strip()
                if user_input in valid_categories:
                    category = user_input
                    cls.vendor_category_map[vendor] = category
                    break
                else:
                    print("Invalid category. Please try again.")

        return category

