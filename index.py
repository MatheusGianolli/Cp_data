import os
import oracledb
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Configuração da conexão usando variáveis de ambiente
def get_connection():
    return oracledb.connect(
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        dsn=os.environ.get("DB_DSN")
    )

# A ROTA ABAIXO DEVE FICAR SEM ESPAÇOS NO INÍCIO
@app.route('/dados')
def listar_dados():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Busca os dados no Banco Oracle
        cursor.execute("SELECT nome, setor, preco_base, estoque FROM TB_ATIVOS_GALACTICOS")
        colunas = [col[0] for col in cursor.description]
        ativos = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify(ativos)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aplicar-evento', methods=['POST'])
def aplicar_evento():
    dados = request.json
    evento_escolhido = dados.get('evento')
    setor_escolhido = dados.get('setor')

    try:
        conn = get_connection()
        cursor = conn.cursor()

        plsql_block = """
        DECLARE
            v_evento VARCHAR2(20) := :tipo;
            v_setor VARCHAR2(20) := :setor;
            v_novo_preco NUMBER;
            CURSOR c_ativos IS
                SELECT id_ativo, preco_base
                FROM TB_ATIVOS_GALACTICOS
                WHERE setor = v_setor;
        BEGIN
            FOR r IN c_ativos LOOP
                IF v_evento = 'RADIACAO' THEN
                    v_novo_preco := r.preco_base * 1.15;
                ELSIF v_evento = 'DESCOBERTA' THEN
                    v_novo_preco := r.preco_base * 0.85;
                ELSE
                    v_novo_preco := r.preco_base;
                END IF;

                UPDATE TB_ATIVOS_GALACTICOS
                SET preco_base = v_novo_preco
                WHERE id_ativo = r.id_ativo;
            END LOOP;
            COMMIT;
        END;
        """
        
        cursor.execute(plsql_block, tipo=evento_escolhido, setor=setor_escolhido)
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Evento aplicado com sucesso no Banco Oracle!"})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
