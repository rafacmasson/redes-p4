class CamadaEnlace:
    ignore_checksum = False

    def __init__(self, linhas_seriais):
        """
        Inicia uma camada de enlace com um ou mais enlaces, cada um conectado
        a uma linha serial distinta. O argumento linhas_seriais é um dicionário
        no formato {ip_outra_ponta: linha_serial}. O ip_outra_ponta é o IP do
        host ou roteador que se encontra na outra ponta do enlace, escrito como
        uma string no formato 'x.y.z.w'. A linha_serial é um objeto da classe
        PTY (vide camadafisica.py) ou de outra classe que implemente os métodos
        registrar_recebedor e enviar.
        """
        self.enlaces = {}
        self.callback = None
        # Constrói um Enlace para cada linha serial
        for ip_outra_ponta, linha_serial in linhas_seriais.items():
            enlace = Enlace(linha_serial)
            self.enlaces[ip_outra_ponta] = enlace
            enlace.registrar_recebedor(self._callback)

    def registrar_recebedor(self, callback):
        """
        Registra uma função para ser chamada quando dados vierem da camada de enlace
        """
        self.callback = callback

    def enviar(self, datagrama, next_hop):
        """
        Envia datagrama para next_hop, onde next_hop é um endereço IPv4
        fornecido como string (no formato x.y.z.w). A camada de enlace se
        responsabilizará por encontrar em qual enlace se encontra o next_hop.
        """
        # Encontra o Enlace capaz de alcançar next_hop e envia por ele
        self.enlaces[next_hop].enviar(datagrama)

    def _callback(self, datagrama):
        if self.callback:
            self.callback(datagrama)


class Enlace:
    def __init__(self, linha_serial):
        self.linha_serial = linha_serial
        self.linha_serial.registrar_recebedor(self.__raw_recv)
        # self.dados_acumulados = b''

    def registrar_recebedor(self, callback):
        self.callback = callback

    def enviar(self, datagrama):
        datagrama_codificado = datagrama.replace(b'\xDB', b'\xDB\xDD').replace(b'\xC0', b'\xDB\xDC')    # Passo 2
        datagrama_codificado = b'\xC0' + datagrama_codificado + b'\xC0' # Passo 1

        self.linha_serial.enviar(datagrama_codificado)

        pass

    def __raw_recv(self, dados):
        # TODO: Preencha aqui com o código para receber dados da linha serial.
        # Trate corretamente as sequências de escape. Quando ler um quadro
        # completo, repasse o datagrama contido nesse quadro para a camada
        # superior chamando self.callback. Cuidado pois o argumento dados pode
        # vir quebrado de várias formas diferentes - por exemplo, podem vir
        # apenas pedaços de um quadro, ou um pedaço de quadro seguido de um
        # pedaço de outro, ou vários quadros de uma vez só.

        dados_lista = dados.split(b'\xc0')
        dados_acumulados = b''

        for item in dados_lista:
            if (item == b''):
                self.callback(dados_acumulados)
                dados_acumulados = b''
            dados_acumulados = dados_acumulados + item
        
        pass
'''
        acumulador = b''
        for i in range(len(dados)):
            if (dados[i:i+1] == b'\xc0' & acumulador != b''):
                self.callback(acumulador)
                acumulador = b''
            else:
                acumulador = acumulador + dados[i:i+1]
'''
        # dados_lista = dados.split(b'\xc0')
        # acumulador = b''

        # if (len(dados_lista) == 1):
        #     if (dados_lista[0] != b''):
        #         acumulador = acumulador + dados_lista[0]
        #     else:
        #         self.callback(acumulador)

        # else:
        #     for item in dados_lista:
        #         if (len(item) != 0): 
        #             self.callback(item)

                # self.dados_acumulados = self.dados_acumulados + item
            # elif (len(self.dados_acumulados) != 0 & len(item) == 0):
                # self.callback(self.dados_acumulados)
                # self.dados_acumulados = b''
        # if (self.dados_acumulados != b''):

        # self.
        # self.residuo_dados = self.residuo_dados + dados
        # self.residuo_dados = self.residuo_dados.split(b'\xC0')

        # if self.residuo_dados[-1] == b'': # todos os dados estão completos
            # self.callback(self.residuo_dados)
        
            # conexao.dados_residuais = conexao.dados_residuais[-1]  # os dados recebidos terminam com uma parte incompleta

