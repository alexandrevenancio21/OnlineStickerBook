import React from 'react';
import ReactDOM from 'react-dom/client';
import {useState, useEffect} from 'react';
import axios from "axios";




const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <CriarPacote/>,
);

 function CriarPacote() {


    const [titulo, setTitulo] = useState('');
    const [descricao, setDescricao] = useState('')
    const [preco, setPreco] = useState('')
    const [qnt_cromos, setqnt_cromos] = useState('')
    const [imagem, setImagem] = useState('/caderneta/Images/Pacotes/default_Pacote.jpg')


    const criarPost = (event) => {
        event.preventDefault() //faz com que nao faça reload ao formulario para poder entrar na loja do site outra vez
        let obj = {
            'titulo': titulo,
            'descricao': descricao,
            'preco': preco,
            'qnt_cromos': qnt_cromos,
            'imagem': imagem
        }

        axios.post("http://localhost:8001/caderneta/api/criar_pacote/", obj)
            .then(res => {
                window.location.href = 'http://127.0.0.1:8001/caderneta/loja';
                }
            );
    }


    return (
        <div className="d-flex justify-content-center align-items-center" style={{height: "100vh"}}>
            <div className="form-signin w-50 m-auto">
                <form onSubmit={criarPost}>

                    <h1 className="h3 mb-3 fw-normal">Criar pacote</h1>
                    <div className="form-floating">
                        <input
                            type="text"
                            className="form-control"
                            value={titulo}
                            onChange={(e) => setTitulo(e.target.value)}
                        />
                        <label htmlFor="titulo">
                            Título:
                        </label>
                    </div>
                    <br/>
                    <div className="form-floating">
                        <input
                            type="text"
                            className="form-control"
                            value={descricao}
                            onChange={(e) => setDescricao(e.target.value)}
                        />
                        <label htmlFor="descricao">
                            Descrição:
                        </label>
                    </div>
                    <br/>
                    <div className="form-floating">
                        <input
                            type="text"
                            className="form-control"
                            value={preco}
                            onChange={(e) => setPreco(e.target.value)}
                        />
                        <label htmlFor={"preco"}>
                            Preço:
                        </label>
                    </div>
                    <br/>
                    <div className="form-floating">
                        <input
                            type="text"
                            className="form-control"
                            value={qnt_cromos}
                            onChange={(e) => setqnt_cromos(e.target.value)}
                        />
                        <label htmlFor={"qnt_cromos"}>
                            Quantidade de Cromos:
                        </label>
                    </div>
                    <br/>
                    <div className="form-floating">
                        <input
                            type="text"
                            className="form-control"
                            value={imagem}
                            onChange={(e) => setImagem(e.target.value)}
                        />
                        <label htmlFor={"imagem"}>
                            URL da Imagem:
                        </label>
                    </div>

                    <br/>
                    <button className="btn btn-primary w-100 py-2" type="submit">Enviar
                    </button>
                </form>
                <p className="mt-5 mb-3 text-body-secondary">©️ 2024 Euro</p>
            </div>
        </div>

    );
 }





