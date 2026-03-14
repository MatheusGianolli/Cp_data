CREATE TABLE TB_ATIVOS_GALACTICOS (
    id_ativo NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(50),
    setor VARCHAR2(20), -- 'MINERAL', 'COMBUSTIVEL', 'DADOS'
    preco_base NUMBER(10,2),
    estoque NUMBER
);

INSERT INTO TB_ATIVOS_GALACTICOS (nome, setor, preco_base, estoque) 
VALUES ('Cristal de Dilítio', 'MINERAL', 500.00, 100);
INSERT INTO TB_ATIVOS_GALACTICOS (nome, setor, preco_base, estoque) 
VALUES ('Hidrogênio Metálico', 'COMBUSTIVEL', 120.00, 500);
INSERT INTO TB_ATIVOS_GALACTICOS (nome, setor, preco_base, estoque) 
VALUES ('Holodiscos de Memória', 'DADOS', 850.00, 50);
COMMIT;

SELECT * FROM TB_ATIVOS_GALACTICOS;

DECLARE
    v_evento VARCHAR2(20) := 'RADIACAO';
    v_setor VARCHAR2(20) := 'MINERAL';
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


