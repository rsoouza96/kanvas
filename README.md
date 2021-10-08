# kanvas

O Kanvas é uma aplicação em Django onde podemos criar cursos, atividades, matricular alunos, editar/atribuir nota para atividades, para isso contamos com três niveis de acesso:
- Estudante;
- Facilitador;
- Instrutor.

#Rotas

```
| Método | Rota | Descrição | Autorização |

| :----: | :---: | :------: | :----------: |

| GET | /api/activities/ | lista atividades do estudante | estudante |

| GET | /api/activities/ | lista todas as atividades de todos os estudantes | facilitador e instrutor |

| GET | /api/activities/<int:user_id>/ | lista todas as atividades de todos os estudantes | facilitador e instrutor |

| POST | /api/activities/ | cria atividade do estudante(sem nota) | estudante |

| POST | /api/courses/ | cria curso | instrutor | 

| POST | /api/login/ | faz autenticação | todos | 

| POST | /api/accounts/ | cria usuários | todos |

| PUT | /api/courses/registrations/ | matricula estudantes num determinado curso | instrutor |

| PUT | /api/activities/ | edita atividade - atribui nota | facilitador e instrutor |
```
