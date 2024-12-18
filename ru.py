import argparse
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from urllib.parse import urlencode
from fake_useragent import UserAgent


class SigaaClient:
    headers = {
        "User-Agent": UserAgent().random,
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "si3.ufc.br",
        "Origin": "https://si3.ufc.br",
        "Referer": "https://www.google.com/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }

    class TipoRefeicao:
        ALMOÇO = (2, 53)
        JANTAR = (3, 54)

    last_page = None
    session = requests.Session()

    def __init__(self):
        self.session.headers.update(self.headers)

    def __del__(self):
        self.session.close()

    def login(self, user: str, password: str):
        paylod = "width=1024&height=768&urlRedirect=&acao=&user.login={}&user.senha={}&entrar=Entrar".format(
            user, password
        )
        url = "https://si3.ufc.br/sigaa/logar.do?dispatch=logOn"
        self.call(
            self.session.post,
            url,
            referer="https://si3.ufc.br/sigaa/verTelaLogin.do",
            payload=paylod,
        )

    def logout(self):
        url = "https://si3.ufc.br/sigaa/logar.do?dispatch=logOff"
        self.call(self.session.get, url, referer=self.last_page.url)

    def tela_inicial(self):
        url = "https://si3.ufc.br/sigaa/paginaInicial.do"
        self.call(
            self.session.get, url, referer="https://si3.ufc.br/sigaa/progresso.jsf"
        )

    def portal_disente(self):
        url = "https://si3.ufc.br/sigaa/verPortalDiscente.do"
        self.call(
            self.session.get, url, referer="https://si3.ufc.br/sigaa/paginaInicial.do"
        )

    def agendamento(self, data: str, tiporefeicao: TipoRefeicao):
        refeicao, horario = tiporefeicao
        soup = BeautifulSoup(self.last_page.content, "html.parser")
        javax_faces = soup.find("input", attrs={"id": "javax.faces.ViewState"}).attrs[
            "value"
        ]
        url = "https://si3.ufc.br/sigaa/ru/form_agendamento.jsf"
        ref = "https://si3.ufc.br/sigaa/portais/discente/discente.jsf"
        payload = urlencode(
            {
                "AJAXREQUEST": "formulario:j_id_jsp_1791888761_3",
                "formulario": "formulario",
                "formulario:data_agendamento": data,
                "formulario:tipo_refeicao": refeicao,
                "formulario:restaurante_universitario": 0,
                "formulario:horario_agendado": 0,
                "javax.faces.ViewState": javax_faces,
                "formulario:j_id_jsp_1791888761_10": "formulario:j_id_jsp_1791888761_10",
            }
        )
        self.call(self.session.post, url, referer=ref, payload=payload)
        payload = urlencode(
            {
                "formulario": "formulario",
                "formulario:data_agendamento": data,
                "formulario:tipo_refeicao": refeicao,
                "formulario:horario_agendado": horario,
                "formulario:cadastrar_agendamento_bt": "Cadastrar Agendamento",
                "javax.faces.ViewState": javax_faces,
            }
        )
        self.call(self.session.post, url, referer=ref, payload=payload)

    def agendamento_pagina(self):
        soup = BeautifulSoup(self.last_page.content, "html.parser")
        disente_id = soup.find("input", {"type": "hidden", "name": "id"}).attrs["value"]
        javax_faces = soup.find("input", attrs={"id": "javax.faces.ViewState"}).attrs[
            "value"
        ]
        payload = "menu:form_menu_discente=menu:form_menu_discente&id={}&jscook_action=menu_form_menu_discente_j_id_jsp_440181972_4_menu:A]#{{ rUAgendamentoMBean.iniciar }}&javax.faces.ViewState={}".format(
            disente_id, javax_faces
        )
        url = ref = "https://si3.ufc.br/sigaa/portais/discente/discente.jsf"
        self.call(self.session.post, url, referer=ref, payload=payload)

    def agendar_semana(self):
        datas = []
        now = datetime.now()
        for i in range(1, 9):
            data = now + timedelta(days=i)
            if data.weekday() < 5:
                datas.append(data.strftime("%d/%m/%Y"))
        for i in datas:
            self.agendamento(i, self.TipoRefeicao.ALMOÇO)
            self.agendamento(i, self.TipoRefeicao.JANTAR)

    def agendar_next_day(self):
        data = datetime.now() + timedelta(days=1)
        while data.weekday() > 4:
            data += timedelta(days=1)
        self.agendamento(data.strftime("%d/%m/%Y"), self.TipoRefeicao.ALMOÇO)
        self.agendamento(data.strftime("%d/%m/%Y"), self.TipoRefeicao.JANTAR)

    def view(self):
        """
        grava no disco a ultima pagina visitada se existir
        """
        if self.last_page != None:
            with open("sigaa.html", "w") as file:
                file.write(self.last_page.text)

    def datas_agendadas(self) -> list[(str, str)]:
        """
        retorna uma lista com as datas que ja estão agendadas.\n
        retorna no formato de uma tupla: ('data','refeição')\n
        é necessario está na pagina de agendamento para usar essa função!
        """
        soup = BeautifulSoup(self.last_page.content, "html.parser")
        datas = [
            (x.contents[1].text, x.contents[3].text)
            for x in soup.findChildren(name="tr")
        ]
        del datas[0]
        return datas

    def call(self, request, url, **kwargs):
        payload = None
        for key in kwargs:
            match key:
                case "referer":
                    self.session.headers["Referer"] = kwargs[key]
                case "payload":
                    payload = kwargs[key]
        self.last_page = request(url, data=payload)


parser = argparse.ArgumentParser(description="Agendador automatico estilo serviço")
parser.add_argument(
    "--modo",
    type=str,
    choices=["week", "next_day"],
    required=True,
    help="define o modo de operação",
)
parser.add_argument("--user", type=str, required=True, help="Seu usuario")
parser.add_argument("--password", type=str, required=True, help="Sua senha")
args = parser.parse_args()
client = SigaaClient()
client.login(args.user,args.password)
client.tela_inicial()
client.portal_disente()
client.agendamento_pagina()
match args.modo:
    case "week":
        client.agendar_semana()
    case "next_day":
        client.agendar_next_day()
client.logout()
