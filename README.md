# Aviso 

Isso é apenas um script de automação, não tem a capacidade de burlar alguma exigência do servidor. 

# Como isso funcionar?
esse script apenas replica as requisições feitas pelo navegador para atingir seus objetivos, sem a necessidade de selenium.

# Execução

instalar dependências:
``` shell
pip install -r requirements.txt
```
modifique conforme necessidade e então execute:
``` shell
python ru.py
```

# Lista de tarefas:

 - [ ] Verificar o status do servidor.
 - [ ] Tentar mais uma vez em caso de erro.
 - [ ]  Verificar os dias já agendados e então decidir os dias para agendar.

# Considerações finais

Seu objetivo principal é ser executado como serviço então busquei algo com minimo de dependências e consumo de memoria. Python foi escolhido por ser multiplataforma.
