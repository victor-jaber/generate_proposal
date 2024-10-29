"use client";

import { useState } from "react";
import styles from './Proposta.module.css';

export default function Proposta() {
    const [itens, setItens] = useState([
        { item: "", descricao: "", qtd: "", unidade: "", unitario: "" }
    ]);

    const handleAddItem = () => {
        setItens([...itens, { item: "", descricao: "", qtd: "", unidade: "", unitario: "" }]);
    };

    const handleRemoveItem = (index) => {
        const newItens = itens.filter((_, i) => i !== index);
        setItens(newItens);
    };

    const handleInputChange = (index, field, value) => {
        const newItens = [...itens];
        newItens[index] = { ...newItens[index], [field]: value };
        setItens(newItens);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        const form = event.target;
        const data = {
            numero_proposta: form.numero_proposta.value,
            cliente: form.cliente.value,
            pessoa_recebe: form.pessoa_recebe.value,
            email_recebe: form.email_recebe.value,
            telefone_recebe: form.telefone_recebe.value,
            obra: form.obra.value,
            objeto_obra: form.objeto_obra.value,
            itens,
            prazo: form.prazo.value,
            condicoes_pagamento: form.condicoes_pagamento.value.split(","),
            responsabilidades_contratada: form.responsabilidades_contratada.value.split(","),
            responsabilidades_contratante: form.responsabilidades_contratante.value.split(","),
        };

        try {
            const response = await fetch('http://localhost:5000/gerar-orcamento', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Orcamento_${data.numero_proposta}.pdf`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a); // Remoção correta do elemento do DOM
        } catch (error) {
            console.error('Erro ao gerar o PDF:', error);
        }
    };

    return (
        <div className={styles.container}>
            <form onSubmit={handleSubmit} className={styles.form}>
                <label htmlFor="numero_proposta">Número da Proposta:</label>
                <input type="text" id="numero_proposta" name="numero_proposta" className={styles.inputField} required />

                <label htmlFor="cliente">Nome do Cliente:</label>
                <input type="text" id="cliente" name="cliente" className={styles.inputField} required />

                <label htmlFor="pessoa_recebe">Pessoa que Receberá:</label>
                <input type="text" id="pessoa_recebe" name="pessoa_recebe" className={styles.inputField} required />

                <label htmlFor="email_recebe">E-mail da Pessoa que Receberá:</label>
                <input type="email" id="email_recebe" name="email_recebe" className={styles.inputField} required />

                <label htmlFor="telefone_recebe">Telefone da Pessoa que Receberá:</label>
                <input type="tel" id="telefone_recebe" name="telefone_recebe" className={styles.inputField} required />

                <label htmlFor="obra">Endereço da Obra:</label>
                <input type="text" id="obra" name="obra" className={styles.inputField} required />

                <label htmlFor="objeto_obra">Objeto da Obra:</label>
                <input type="text" id="objeto_obra" name="objeto_obra" className={styles.inputField} required />

                <h3>Itens do Orçamento</h3>
                <table className={styles.table}>
                    <thead>
                        <tr>
                            <th>Item</th>
                            <th>Descrição</th>
                            <th>Quantidade</th>
                            <th>Unidade</th>
                            <th>Valor Unitário</th>
                            <th>Ação</th>
                        </tr>
                    </thead>
                    <tbody>
                        {itens.map((item, index) => (
                            <tr key={index}>
                                <td><input type="text" value={item.item} onChange={e => handleInputChange(index, "item", e.target.value)} className={styles.inputField} required /></td>
                                <td><input type="text" value={item.descricao} onChange={e => handleInputChange(index, "descricao", e.target.value)} className={styles.inputField} required /></td>
                                <td><input type="number" value={item.qtd} onChange={e => handleInputChange(index, "qtd", e.target.value)} className={styles.inputField} required /></td>
                                <td><input type="text" value={item.unidade} onChange={e => handleInputChange(index, "unidade", e.target.value)} className={styles.inputField} required /></td>
                                <td><input type="number" value={item.unitario} onChange={e => handleInputChange(index, "unitario", e.target.value)} className={styles.inputField} required /></td>
                                <td><button type="button" className={styles.removeItemBtn} onClick={() => handleRemoveItem(index)}>Remover</button></td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                <div>
                    <button type="button" className={styles.addItemBtn} onClick={handleAddItem}>
                        Adicionar Item
                    </button>
                </div>
                <div className={styles.inputGroup}>
                    <label htmlFor="prazo">Prazo:</label>
                    <input type="text" id="prazo" name="prazo" className={styles.inputField} required />
                </div>

                <textarea id="condicoes_pagamento" name="condicoes_pagamento" className={styles.textareaField} rows={3} defaultValue="30 dias após entrega, Pagamento via boleto bancário" required />

                <textarea id="responsabilidades_contratada" name="responsabilidades_contratada" className={styles.textareaField} rows={3} defaultValue="Fornecer todo material necessário, Cumprir os prazos estabelecidos" required />

                <textarea id="responsabilidades_contratante" name="responsabilidades_contratante" className={styles.textareaField} rows={3} defaultValue="Prover acesso ao local da obra, Realizar o pagamento nas datas acordadas" required />

                <button type="submit" className={styles.submitButton}>Gerar Proposta</button>
            </form>
        </div>
    );
}
