

---

# Conversor de Contatos VCard para PDF

Este script Python lê arquivos VCard (VCF) contendo informações de contato e gera um arquivo PDF listando os contatos. Ele também remove números de telefone duplicados.

## Requisitos

- Python 3.x instalado
- Biblioteca `reportlab` (para gerar o PDF)

## Como Usar

1. Clone este repositório:

   ```bash
   git clone https://github.com/Ricardo-SS/Convert_VCF_To_PDF.git
   ```

2. Instale a biblioteca `reportlab`:

   ```bash
   pip install reportlab
   ```

3. Execute o script:

   ```bash
   python vcard_to_pdf.py arquivo1.vcf arquivo2.vcf ...
   ```

   O script processará os arquivos VCard especificados e criará um arquivo `contatos.pdf` com os nomes e números dos contatos.

## Exemplo de Saída

O arquivo `contatos.pdf` conterá uma lista de contatos no seguinte formato:

```
1. Nome: João Silva
   Tel: +55 11 1234-5678
   Email: joao@example.com
2. Nome: Maria Santos
   Celular: +55 21 9876-5432
   Email: maria@example.com
...
```

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.  😊🚀

---
