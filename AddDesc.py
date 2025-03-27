from pydantic import BaseModel
from openai import OpenAI
import sys
import argparse
import colorama
from colorama import Fore, Style
import os

colorama.init()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

class AttributeDescription(BaseModel):
    # attribute names don't change but descriptions written by AI
    attribute_names: list[str]
    descriptions: list[str]

def generate_all_attribute_descriptions(attributes_text, model, prompt):
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": attributes_text},
        ],
        response_format=AttributeDescription,
    )
    return completion.choices[0].message.parsed

def print_header():
            print(Fore.LIGHTGREEN_EX + """
        ###############################################################
        #                                                             #      
        #   Welcome to AURA - Automated Universal Row Augmenter       #
        #   v1.0a - Created by Alper Baykara                          #
        #                                                             #
        #   Pre-Configured for adding Turkish descriptions            #
        #   for database attributes                                   #
        #                                                             #
        #   Usage: AddDesc.exe <input_file> <output_file>             #
        #                                                             #
        #   E.g:                                                      #
        #        Customer ID                                          #
        #        Customer Name                                        #
        #                                                             #
        #        ↓                                                    #
        #                                                             #
        #        Customer ID: Müşteri Tekil Anahtarı                  #
        #        Customer Name: Müşteri Adı                           #
        #                                                             #
        ###############################################################

          """ + Style.RESET_ALL)


def main(input_file, output_file, model, prompt, chunk_size):
            
    # Read all lines from the input file
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Process every chunk_size lines as a separate chunk
    input_chunks = ["".join(lines[i:i+chunk_size]) for i in range(0, len(lines), chunk_size)]
    total_chunks = len(input_chunks)
    all_mappings = []

    for idx, chunk in enumerate(input_chunks, start=1):
        result = generate_all_attribute_descriptions(chunk, model, prompt)
        # Ensure ordering by pairing attribute names and descriptions as returned in each chunk.
        mapped = [f"{attr}: {desc}" for attr, desc in zip(result.attribute_names, result.descriptions)]
        all_mappings.extend(mapped)

        # Display a simple text-based progress bar
        progress = int((idx / total_chunks) * 100)
        print(f"Processing chunk {idx}/{total_chunks}... {progress}% complete")
        
        # Save progress in the output file after each request
        with open(output_file, "w", encoding="utf-8") as fdesc:
            fdesc.write("\n".join(all_mappings))
    
    print(f"Descriptions saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Attribute Description Generator")
    parser.add_argument("input_file", nargs='?', help="Input file containing attributes")
    parser.add_argument("output_file", nargs='?', help="Output file for attribute descriptions")
    parser.add_argument("--debug", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--model", default="gpt-4o-mini", help=argparse.SUPPRESS)
    parser.add_argument("--prompt", default="Sen bir veri modelleme uzmanısın, ingilizce gördüğün attribute alanlarının karşısına türkçe bir açıklama yaz. sadece 2-3 kelimelik bir cümle olarak. ID kelimesini veya ingilizce kelimeler kullanma. PK veya FK lar için Tekil anahtarı veya Dış Anahtarı tabirini kullan örnek: Customer ID -> Müşteri Tekil Anahtarı. Bayrak yerine bilgisi de, örnek: KVKK Flag -> KVKK bilgisi.  Accepted Commission Amount: Kabul Edilen Komisyon Tutarı", help=argparse.SUPPRESS)
    parser.add_argument("--chunk_size", type=int, default=100, help=argparse.SUPPRESS)

    args = parser.parse_args()

    if not args.input_file or not args.output_file:
        print_header()

        if args.debug:
            print(Fore.RED + f"### Warning: Debug mode is an *EXPERIMENTAL* feature. Use at your own risk. ###\n" + Style.RESET_ALL)

        input_file = input("Please enter the input file path: ")
        output_file = input("Please enter the output file path: ")
        model = "gpt-4o-mini"
        prompt = "Sen bir veri modelleme uzmanısın, ingilizce gördüğün attribute alanlarının karşısına türkçe bir açıklama yaz. sadece 2-3 kelimelik bir cümle olarak. ID kelimesini veya ingilizce kelimeler kullanma. PK veya FK lar için Tekil anahtarı veya Dış Anahtarı tabirini kullan örnek: Customer ID -> Müşteri Tekil Anahtarı. Bayrak yerine bilgisi de, örnek: KVKK Flag -> KVKK bilgisi.  Accepted Commission Amount: Kabul Edilen Komisyon Tutarı"
        chunk_size = 100

        if args.debug:
            model = input(f"Please enter the model (default: {model}): ") or model
            prompt = input(f"Please enter the prompt or press enter for default prompt: ") or prompt
            chunk_size = int(input(f"Please enter the chunk size (default: {chunk_size}): ") or chunk_size)

        confirm = input("Do you want to proceed with these settings? (yes/no): ")
        # can be yes or Y or y etc. and enter also means yes
        if confirm.lower() in ["yes", "y", ""]:
            print("Processing...")
            main(input_file, output_file, model, prompt, chunk_size)
        else:
            print("Operation cancelled.")
            sys.exit(1)


    else:
        print_header()
        if args.debug:
            print(Fore.RED + f"### Warning: Debug mode is an *EXPERIMENTAL* feature. Use at your own risk. ###\n" + Style.RESET_ALL)
            main(args.input_file, args.output_file, args.model, args.prompt, args.chunk_size)
        else:
            if any(arg in sys.argv for arg in ["--model", "--prompt", "--chunk_size"]):
                print("Error: --model, --prompt, and --chunk_size can only be used with --debug")
                sys.exit(1)
            main(args.input_file, args.output_file, "gpt-4o-mini", "Sen bir veri modelleme uzmanısın, ingilizce gördüğün attribute alanlarının karşısına türkçe bir açıklama yaz. sadece 2-3 kelimelik bir cümle olarak. ID kelimesini veya ingilizce kelimeler kullanma. PK veya FK lar için Tekil anahtarı veya Dış Anahtarı tabirini kullan örnek: Customer ID -> Müşteri Tekil Anahtarı. Bayrak yerine bilgisi de, örnek: KVKK Flag -> KVKK bilgisi.  Accepted Commission Amount: Kabul Edilen Komisyon Tutarı", 100)