1 - Descrição Geral 

A atividade prática da disciplina consiste em desenvolver uma aplicação de videoconferência descentralizada. Para isso, deve ser utilizada comunicação por sockets, permitindo que os usuários primeiro se registrem em um servidor e consultem a lista de nós cadastrados, para depois de conectarem aos seus pares utilizando o modelo Peer-to-Peer (P2P).

2 - Desenvolvimento 

O desenvolvimento e a avaliação da atividade serão realizados em duas etapas:

ETAPA 1: Registro e consultas no servidor 

Nesta etapa, é necessário implementar um socket TCP que interconecte os clientes e o servidor.

O socket cliente deve:
Registrar-se no servidor utilizando um nome e um IP exclusivos e indicando a porta apta para receber o pedido de chamada;
Realizar consultas de endereços de portas por nomes específicos dos usuários;
Caso o cliente deseje se desvincular do servidor de registro, ele deve enviar uma mensagem com esta solicitação.


O socket servidor deve:
Armazenar e imprimir uma tabela dinâmica contendo informações dos clientes;
Imprimir mensagem de confirmação de registro de novo usuário;
Caso o usuário já esteja cadastrado, imprimir mensagem informando esta condição;
Responder aos clientes o nome de um nó conectado e seus respectivos endereços e números de porta, quando assim solicitado;
Caso o cliente solicite o fim da conexão, o servidor deve responder com mensagem de encerramento e, depois, fechar o socket.


Data de entrega: 31/10/2023


ETAPA 2: Implementação do serviço 

Nesta etapa, deve ser implementada a lógica do serviço.

O socket cliente deve:
Solicitar a videochamada a um par IP:porta de destino utilizando uma mensagem específica, como se fosse a mensagem de INVITE do protocolo SIP. Assim, o receptor pode negar ou aceitar o pedido;
A reprodução da mídia deve ser iniciada assim que a chamada é aceita;
Conter métodos para encerrar a transmissão.



O socket servidor deve: 
Aceitar ou rejeitar a chamada;
Se a chamada for aceita, informar na resposta o número das portas para receber os fluxos de áudio e vídeo.



Data de entrega: 28/11/2023

3 - Entregáveis

No Google Classroom, deve ser entregue um arquivo .zip contendo:
Código da aplicação comentado e respeitando as boas práticas de programação;
Relatório técnico, em formato .pdf, explicando detalhadamente a implementação e o uso da aplicação. Deve especificar ainda quais atividades foram realizadas pelos integrantes do grupo.



OBS: A falta de especificação detalhada de como executar os códigos e os consequentes erros gerados a partir disso irão incorrer em nota ZERO na atividade.

4 - Apresentação 

Na data definida para a entrega de cada etapa, deve ser feita uma apresentação oral do trabalho com duração de 5 a 7 minutos, incluindo uma demonstração da aplicação em funcionamento.

5 - Recomendações 
O trabalho pode ser realizado em grupo de três alunos;
Implementação na linguagem Python;
Podem ser utilizadas bibliotecas de preferência dos alunos, desde que explicadas no relatório;
Interfaces gráficas não são obrigatórias, mas contarão como pontos extras;
Tratativas de latência, perda de pacotes e afins não são obrigatórias, mas contarão como pontos extras;
vidstream: https://pypi.org/project/vidstream/
gstreamer: https://gstreamer.freedesktop.org/documentation/installing/index.html?gi-language=c
PyAudio: https://pypi.org/project/PyAudio/
OpenCV: https://pypi.org/project/opencv-python/
RTP: https://pypi.org/project/rtp/


6 - Critérios de Avaliação 
A nota de cada etapa será constituída pela média aritmética simples das notas de cada tarefa;
A nota final será a média aritmética simples das duas etapas.


7 - Considerações Finais 
               
Em caso de dúvidas, os alunos podem consultar o monitor da disciplina de forma presencial ou remota todas as quintas-feiras, das 16h às 17h, ou podem fazer contato pelo classroom ou  pelo e-mail romulo_vieira@midiacom.uff.br.
Link da videochamada: https://meet.google.com/vjy-jsra-pmk
