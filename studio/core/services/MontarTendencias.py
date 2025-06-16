import calendar

def montarTendencias(dicio):
    novas = {}
    renovacoes = {}
    cancelados = {}

    for i in dicio['novas_assinaturas']:
        novas[i["_id"]] = i.get('qtd')

    for i in dicio['renovacoes']:
        renovacoes[i["_id"]] = i.get('qtd')

    for i in dicio['cancelamentos']:
        cancelados[i["_id"]] = i.get('qtd')

    tendenciaMeses = [
        {
            'mes': calendar.month_name[i],
            'novas': novas.get(i, 0),
            'renovacoes': renovacoes.get(i, 0),
            'cancelados': cancelados.get(i, 0)

        }
        for i in range(1, 12)
    ]

    return tendenciaMeses