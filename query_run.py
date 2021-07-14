import query

if __name__ == '__main__':
    print("\n==================== Start query ====================")
    query.f.truncate()
    info_need1 = 'which researchers at Concordia worked on COVID 19-related research?'
    info_need2 = 'which departments at Concordia have research in environmental issues, sustainability, energy and water conservation?'
    query.f.write("Information need: " + info_need1 + "\n")
    print("Information need: " + info_need2)
    query.f.write("Information need: " + info_need2 + "\n")

    query1 = 'covid-19 research'
    query2 = 'researchers worked on covid-19'
    query.probabilistic_search_engine(query1)
    query.probabilistic_search_engine(query2)

    query3 = 'department studies environmental issues'
    query4 = 'research on sustainability, energy and water conservation'
    query.probabilistic_search_engine(query3)
    query.probabilistic_search_engine(query4)

    print("\n==================== Start challenge query ====================")
    query.f.write("\n==================== challenge query ====================\n")

    challenge_query1 = "water management sustainability Concordia"

    challenge_query2 = "Concordia COVID-19 faculty"

    challenge_query3 = "SARS-CoV Concordia faculty"

    query.probabilistic_search_engine(challenge_query1)
    query.probabilistic_search_engine(challenge_query2)
    query.probabilistic_search_engine(challenge_query3)
