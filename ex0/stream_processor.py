from abc import ABC , abstractmethod
from typing import Any, List, Union, TypeAlias

NumericValue: TypeAlias = Union[int, float]
class DataProcessor(ABC):
        def __init__(self,name:str, validation_label)->None:
                self.name: str = name
                self.validation_label: str = validation_label
        
        @abstractmethod
        def process(self,data:Any)->str:
                raise NotImplementedError

        @abstractmethod
        def validate(self, data:Any) -> bool:
                raise NotImplementedError

        def format_output(self, result: str)->str:
                return result


class NumericProcessor(DataProcessor):
        def __init__(self)->None:
               super().__init__("Numeric Processor","Numeric Data verified")
        
        def validate(self, data:Any)->bool:
                if not isinstance(data,list):
                        return False
                return all(
                isinstance(value, (int, float)) and not isinstance(value, bool) 
                for value in data )

        def process(self, data)->str:

                if not self.validate(data):
                      raise ValueError("NumericProcessor expects a list of int or float values. ")
                
                numbers: list[NumericValue] = data

                total: NumericValue = sum(numbers)
                average: float =  float(total) / len(numbers) if numbers else 0.0

                return(
                        f"Processed {len(numbers)} numeric value, "
                        f"sum={total}, avg={average}"
                )
        
        def format_output(self, result:str)->str:
                return result



class TextProcessor(DataProcessor):
        def __init__(self):
                super().__init__("Text Process","Text Data verified")
        
        def validate(self, data:Any)->bool:
                if not isinstance(data,str):
                        return False
                return True
        
        def process(self, data:str)-> str:
                
                if not self.validate(data):
                        raise ValueError("TextProcessor excpect a string values. ")

                total_char = len(data)
                total_word = len(data.split())
                return(f"Processed text: {total_char} characters, {total_word} words")

        def format_output(self, result:str):
                return result
                

class LogProcessor(DataProcessor):
        def __init__(self,)->None:
                super().__init__("Log Processor", "Log entry verified")

        def validate(self, data:Any)->bool:
                if not isinstance(data,str):
                        return False
                if ":" not in data:
                        return False
                
                level, message =  data.split(":",1)
                return bool(level.strip()) and bool(message.strip())
        
        def process(self, data:Any)->str:
                if not self.validate(data):
                        raise ValueError("LogProcessor expects data like 'LEVEL: message'.")                
                level,message = data.split(":",1)
                self.clean_level:str = level.strip().upper()
                self.clean_message:str=message.strip()

                return f"{self.clean_level} level detected: {self.clean_message}"
        def format_output(self, result:str)->str:
                if self.clean_level == "ERROR":
                        return f"[ALERT] {result}"
                if self.clean_level == "INFO":
                        return f"[INFO] {result}"
                if self.clean_level == "WARNING":
                        return f"[WARNING] { result}"
                return result

def main()->None:

        print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")

        print("Initializing Numeric Processor...")
        N_processor = NumericProcessor()
        N_data = [1, 2, 3, 4, 5]
        print(f"Processing Data: {N_data}")

        if N_processor.validate(N_data):
                print(f"Validation: {N_processor.validation_label}")
                N_result = N_processor.process(N_data)
                print(f"Output: {N_processor.format_output(N_result)}")

        print("\nInitializing Text Processor...")        
        T_data="ilyas"
        T_processor = TextProcessor()
        print(f"Processing data: {T_data}")
        if T_processor.validate(T_data):
                print(f"Validation: {T_processor.validation_label}")
                T_result = T_processor.process(T_data)
                print(T_processor.format_output(T_result))
        
        print("\nInitializing Log Processor...")
        L_Data = "INFO: Connection timeout "
        L_processor = LogProcessor()

        if L_processor.validate(L_Data):
                L_result= L_processor.format_output(L_processor.process(L_Data))
                print(f"Processing data: {L_processor.clean_level}: {L_processor.clean_message} ")
                print("Validation: Log every verified")
                print(f"Ouput:{L_result}")
        
        print("\n=== Polymorphic Processing Demo ===")

        print("Processing multiple data types through same interface...")
        test_data = [
            [1, 2, 3],                  
            "Hello Nexus",              
            "INFO: System ready"        
        ]

        all_processors: List[DataProcessor] = [NumericProcessor(), TextProcessor(), LogProcessor()]
        test_data = [[1, 2, 3], "Hello Nexus", "ERROR: System failure"]

        for i in range(len(all_processors)):
            res = all_processors[i].process(test_data[i])
            print(f"Result {i+1}: {res}")

if __name__ =="__main__":
        main()
