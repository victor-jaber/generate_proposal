from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  
from generate_proposal.generateProposal import gerar_orcamento



app = Flask(__name__)
CORS(app)  

@app.route('/gerar-orcamento', methods=['POST'])
def gerar_orcamento_api():
    data = request.json
    try:
        # Gera o PDF e retorna o buffer (BytesIO)
        pdf_buffer = gerar_orcamento(
            data['numero_proposta'],
            data['cliente'],
            data['pessoa_recebe'],
            data['email_recebe'],
            data['telefone_recebe'],
            data['obra'],
            data['objeto_obra'],
            data['itens'],
            data['prazo'],
            data['condicoes_pagamento'],
            data['responsabilidades_contratada'],
            data['responsabilidades_contratante']
        )
        
        # Envia o arquivo gerado para download, ajustando o nome e o mimetype
        return send_file(
            pdf_buffer, 
            as_attachment=True, 
            download_name=f"Orcamento_{data['numero_proposta']}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        print(f"Erro ao gerar PDF: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
