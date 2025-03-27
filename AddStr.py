from pydantic import BaseModel
from openai import OpenAI
import sys
import argparse
import colorama
from colorama import Fore, Style

colorama.init()

client = OpenAI()

class AttributeDescription(BaseModel):
    # attribute names don't change but descriptions written by AI
    entity_name: str
    attribute_names: list[str]
    descriptions: list[str]

def generate_all_attribute_descriptions(entity_name, attributes_text, model, prompt):
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Entity Name: " + entity_name + "\n" + attributes_text},
        ],
        response_format=AttributeDescription,
    )
    return completion.choices[0].message.parsed

def print_header():
            print(Fore.LIGHTGREEN_EX + """
        ################################################################
        #                                                              #      
        #   Welcome to AURA - Automated Universal Row Augmenter        #
        #   v1.0b - Created by Alper Baykara                           #
        #                                                              #
        #   Pre-Configured for adding Stereotypes                      #
        #   for database attributes                                    #
        #                                                              #
        #   Usage: AddStr.exe <Entity Name> <input_file> <output_file> #
        #                                                              #
        #   E.g:                                                       #
        #        <Customer>                                            #
        #                                                              #          
        #        Customer ID                                           #
        #        Customer Middle Name                                  #
        #                                                              #
        #        ↓                                                     #
        #                                                              #
        #        Customer ID: core                                     #
        #        Customer Middle Name: -                               #
        #                                                              #
        ################################################################

          """ + Style.RESET_ALL)


def main(entity_name, input_file, output_file, model, prompt, chunk_size):
            
    # Read all lines from the input file
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Process every chunk_size lines as a separate chunk
    input_chunks = ["".join(lines[i:i+chunk_size]) for i in range(0, len(lines), chunk_size)]
    total_chunks = len(input_chunks)
    all_mappings = []

    for idx, chunk in enumerate(input_chunks, start=1):
        result = generate_all_attribute_descriptions(entity_name, chunk, model, prompt)
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
    parser = argparse.ArgumentParser(description="Stereotype Generator")
    parser.add_argument("entity_name", nargs='?', help="Entity name where the attributes belong")
    parser.add_argument("input_file", nargs='?', help="Input file containing attributes")
    parser.add_argument("output_file", nargs='?', help="Output file for attribute descriptions")
    parser.add_argument("--debug", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--model", default="gpt-4o", help=argparse.SUPPRESS)
    parser.add_argument("--prompt", default="You are a data modeling expert working on a banking data model, based on the entity name and attribute, write 'stereotypes' depending on type of attribute. if the attribute must be in the model, write 'core', if it is not necessary, write empty string '', if it is an attribute that is specific for a local language or system, write 'local'. Example: Fact Customer;Customer ID;core  Fact Overdraft Contract;Contract Description;'' Dim City;side for istanbul;local", help=argparse.SUPPRESS)
    parser.add_argument("--chunk_size", type=int, default=100, help=argparse.SUPPRESS)

    args = parser.parse_args()

    if not args.entity_name or not args.input_file or not args.output_file:
        print_header()

        if args.debug:
            print(Fore.RED + f"### Warning: Debug mode is an *EXPERIMENTAL* feature. Use at your own risk. ###\n" + Style.RESET_ALL)

        entity_name = input("Please enter the entity name: ")
        input_file = input("Please enter the input file path: ")
        output_file = input("Please enter the output file path: ")
        model = "gpt-4o"
        prompt = "You are a data modeling expert working on a banking data model, based on the entity name and attribute, write 'stereotypes' depending on type of attribute. if the attribute must be in the model, write 'core', if it is not necessary, write empty string '', if it is an attribute that is specific for a local language or system, write 'local'. Example: Fact Customer;Customer ID;core  Fact Overdraft Contract;Contract Description;'' Dim City;side for istanbul;local"
        chunk_size = 100

        if args.debug:
            model = input(f"Please enter the model (default: {model}): ") or model
            prompt = input(f"Please enter the prompt or press enter for default prompt: ") or prompt
            chunk_size = int(input(f"Please enter the chunk size (default: {chunk_size}): ") or chunk_size)

        confirm = input("Do you want to proceed with these settings? (yes/no): ")
        # can be yes or Y or y etc. and enter also means yes
        if confirm.lower() in ["yes", "y", ""]:
            print("Processing...")
            main(entity_name, input_file, output_file, model, prompt, chunk_size)
        else:
            print("Operation cancelled.")
            sys.exit(1)


    else:
        print_header()
        if args.debug:
            print(Fore.RED + f"### Warning: Debug mode is an *EXPERIMENTAL* feature. Use at your own risk. ###\n" + Style.RESET_ALL)
            main(args.entity_name, args.input_file, args.output_file, args.model, args.prompt, args.chunk_size)
        else:
            if any(arg in sys.argv for arg in ["--model", "--prompt", "--chunk_size"]):
                print("Error: --model, --prompt, and --chunk_size can only be used with --debug")
                sys.exit(1)
            main(args.entity_name, args.input_file, args.output_file, "gpt-4o", "You are a data modeling expert working on a banking data model, based on the entity name and attribute, write 'stereotypes' depending on type of attribute. if the attribute must be in the model, write 'core', if it is not necessary, write empty string '', if it is an attribute that is specific for a local language or system, write 'local'. Example: Fact Customer;Customer ID;core  Fact Overdraft Contract;Contract Description;'' Dim City;side for istanbul;local", 100)