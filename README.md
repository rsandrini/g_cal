g_cal
=====


G_CAL 0.2 Integra com o calendário do google na versão 3 da api. É Necessario ter e client_id e cliente_secret para autenticar. Veja em https://code.google.com/apis/console/ seus dados

Infos: Altere no /admin os dados de (site) para que ele tenha a referencia correta na hora de executar a STEP2 da autenticação.

Funcionamento: Após o cliente autorizar o acesso do APP na conta google ele registra a credencial no banco. Este processo funciona apenas com as bibliotecas mais atuais do google calendar para python Na versão "baixavel" deles na data de hoje (24/08/2012) ainda apresenta problemas, tive que atualizar manualmente as bibliotecas do Python para conseguir rodar o projeto corretamente.

Os metodos, chamadas, atributos etc podem ser consultados em: https://developers.google.com/google-apps/calendar/?hl=pt-BR

Versões deste app podem ser vistos em: https://github.com/rafilsk/g_cal

Este código ainda é beta e precisa de muita refatoração, foi apenas para demonstrar e entender o funcionando da autenticação e troca de informações atraves do protocolos do google.
