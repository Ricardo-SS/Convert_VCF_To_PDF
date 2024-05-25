import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import glob

# Ler varios arquivo de contato VCF e tranforma em PDF listando os contatos

def read_vcf(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    
    # Split the data into separate vcards
    vcards = data.split("END:VCARD")
    
    contacts = []
    for vcard in vcards:
        contact = {}
        if "BEGIN:VCARD" in vcard:
            # Extract FN (Full Name)
            fn_match = re.search(r'FN:(.*)', vcard)
            if fn_match:
                contact['Full Name'] = fn_match.group(1).strip()
            
            # Extract N (Name)
            n_match = re.search(r'N:(.*)', vcard)
            if n_match:
                contact['Name'] = n_match.group(1).strip()
            
            # Extract TEL (Telephone) with category
            tel_matches = re.findall(r'TEL(;[^:]+)?:(\+?[0-9 -]+)', vcard)
            phones = []
            for match in tel_matches:
                type_info = match[0].replace(';', '').replace('waid=', '')
                if 'Celular' in type_info:
                    type_info = 'Celular'
                else:
                    type_info = 'Tel'
                number = match[1].strip()
                phones.append({"Type": type_info, "Number": number})
            
            # Remove duplicate numbers if they are categorized differently but are the same
            unique_phones = []
            seen_numbers = set()
            for phone in phones:
                if phone["Number"] not in seen_numbers:
                    unique_phones.append(phone)
                    seen_numbers.add(phone["Number"])
            
            if unique_phones:
                contact['Phones'] = unique_phones
            
            # Extract EMAIL
            email_matches = re.findall(r'EMAIL(;[^:]+)?:(.*)', vcard)
            if email_matches:
                contact['Emails'] = [match[1].strip() for match in email_matches]
            
            contacts.append(contact)
    
    return contacts

def merge_contacts(contact_lists):
    merged_contacts = []
    seen_numbers = set()
    
    for contacts in contact_lists:
        for contact in contacts:
            # Check if any phone number is already in the seen_numbers set
            is_duplicate = False
            for phone in contact.get('Phones', []):
                if phone['Number'] in seen_numbers:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                merged_contacts.append(contact)
                # Add the phone numbers of this contact to seen_numbers
                for phone in contact.get('Phones', []):
                    seen_numbers.add(phone['Number'])
    
    # Sort merged contacts by Full Name
    merged_contacts.sort(key=lambda x: x.get('Full Name', '').lower())
    
    return merged_contacts

def print_contacts(contacts):
    for i, contact in enumerate(contacts, start=1):
        print(f"{i}. Nome: {contact.get('Full Name', 'N/A')}")
        for phone in contact.get('Phones', []):
            type_ = phone.get('Type', 'N/A').capitalize()
            if type_ == 'Celular':
                print(f"   Celular: {phone.get('Number', 'N/A')}")
            else:
                print(f"   Tel: {phone.get('Number', 'N/A')}")
        for email in contact.get('Emails', []):
            print(f"   Email: {email}")
        print("-" * 40)

def generate_pdf(contacts, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 10)
    
    margin = 30
    col_width = (width - 2 * margin) / 2
    y_start = height - 40
    y = y_start
    col = 0
    
    for i, contact in enumerate(contacts, start=1):
        x = margin + col * col_width
        c.drawString(x, y, f"{i}. Nome: {contact.get('Full Name', 'N/A')}")
        y -= 15
        for phone in contact.get('Phones', []):
            type_ = phone.get('Type', 'N/A').capitalize()
            if type_ == 'Celular':
                c.drawString(x, y, f"   Celular: {phone.get('Number', 'N/A')}")
            else:
                c.drawString(x, y, f"   Tel: {phone.get('Number', 'N/A')}")
            y -= 15
        for email in contact.get('Emails', []):
            c.drawString(x, y, f"   Email: {email}")
            y -= 15
        y -= 15  # Add some space between contacts
        
        if y < 40:  # Check if we need a new page
            if col == 0:  # Switch to the second column
                col = 1
                y = y_start
            else:  # Add a new page
                c.showPage()
                c.setFont("Helvetica", 10)
                y = y_start
                col = 0
    
    c.save()

# Paths to the vcf files
file_paths = glob.glob('*.vcf')
pdf_path = 'contatos.pdf'

all_contacts = []
for file_path in file_paths:
    contacts = read_vcf(file_path)
    all_contacts.append(contacts)

merged_contacts = merge_contacts(all_contacts)
print_contacts(merged_contacts)
generate_pdf(merged_contacts, pdf_path)

print(f"PDF gerado: {pdf_path}")
