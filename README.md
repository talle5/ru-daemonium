# Aviso 

Isso é apenas um script de automação, não tem a capacidade de burlar alguma exigência do servidor. 

# Como isso funcionar?
esse script apenas replica as requisições feitas pelo navegador para atingir seus objetivos, sem a necessidade de selenium.

# Execução

instalar dependências:
``` shell
pip install -r requirements.txt
```
execute:
``` shell
python ru.py --modo [week,next_day] --user [USUARIO] --password [SENHA]
```

# Automação completa com GitHubActions
1. fork esse repositório 
2. adicione seus segredos ao repositorio: <br/>SIGAA_USER = seu usuário <br/>SIGAA_SENHA = sua senha
3. modifique a data e horário pra a execução do script em .github/workflows/main.yml
4. e pronto!


# Lista de tarefas:

 - [ ] Verificar o status do servidor.
 - [ ] Tentar mais uma vez em caso de erro.
 - [ ]  Verificar os dias já agendados e então decidir os dias para agendar.

# Considerações finais

Seu objetivo principal é ser executado como serviço então busquei algo com minimo de dependências e consumo de memoria. Python foi escolhido por ser multiplataforma.
