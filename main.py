import requests
from classes import axie_class

url = "https://graphql-gateway.axieinfinity.com/graphql"

axie_id = int(input("Enter Axie id: "))
enemy_class = int(input("Type of Enemy\n'1'Plant/Reptile/Dusk\n'2'Beast/Bird/Mech\n'3'Aqua/Bird/Dawn\n"))

data = {
    "operationName": "GetAxieDetail",
    "variables": {
        "axieId": axie_id
    },
    "query": "query GetAxieDetail($axieId: ID!) {\n  axie(axieId: $axieId) {\n    ...AxieDetail\n    __typename\n  }\n}\n\nfragment AxieDetail on Axie {\n  id\n  image\n  class\n  chain\n  name\n  genes\n  owner\n  birthDate\n  bodyShape\n  class\n  sireId\n  sireClass\n  matronId\n  matronClass\n  stage\n  title\n  breedCount\n  level\n  figure {\n    atlas\n    model\n    image\n    __typename\n  }\n  parts {\n    ...AxiePart\n    __typename\n  }\n  stats {\n    ...AxieStats\n    __typename\n  }\n  auction {\n    ...AxieAuction\n    __typename\n  }\n  ownerProfile {\n    name\n    __typename\n  }\n  battleInfo {\n    ...AxieBattleInfo\n    __typename\n  }\n  children {\n    id\n    name\n    class\n    image\n    title\n    stage\n    __typename\n  }\n  __typename\n}\n\nfragment AxieBattleInfo on AxieBattleInfo {\n  banned\n  banUntil\n  level\n  __typename\n}\n\nfragment AxiePart on AxiePart {\n  id\n  name\n  class\n  type\n  specialGenes\n  stage\n  abilities {\n    ...AxieCardAbility\n    __typename\n  }\n  __typename\n}\n\nfragment AxieCardAbility on AxieCardAbility {\n  id\n  name\n  attack\n  defense\n  energy\n  description\n  backgroundUrl\n  effectIconUrl\n  __typename\n}\n\nfragment AxieStats on AxieStats {\n  hp\n  speed\n  skill\n  morale\n  __typename\n}\n\nfragment AxieAuction on Auction {\n  startingPrice\n  endingPrice\n  startingTimestamp\n  endingTimestamp\n  duration\n  timeLeft\n  currentPrice\n  currentPriceUSD\n  suggestedPrice\n  seller\n  listingIndex\n  state\n  __typename\n}\n"
}

data = requests.post(url, json=data)
response_data = data.json()

skills = {}
multiplier = 0
end_turn = False

def class_multiplier(enemy_class):
    global multiplier
    for k, v in axie_class.items():
        for i in skill_type:
            if i in v:
                if int(k) == enemy_class:
                    multiplier = 0.10
                    return multiplier
                elif int(k) == 1 and enemy_class == 2:
                    multiplier = -0.15
                    return multiplier
                elif int(k) == 2 and enemy_class == 3:
                    multiplier = -0.15
                    return multiplier
                elif int(k) == 3 and enemy_class == 1:
                    multiplier = -0.15
                    return multiplier
                elif int(k) == 3 and enemy_class == 2:
                    multiplier = 0.15
                    return multiplier
                elif int(k) == 2 and enemy_class == 1:
                    multiplier = 0.15
                    return multiplier
                elif int(k) == 1 and enemy_class == 3:
                    multiplier = 0.15
                    return multiplier


for i in range(2, 6):
    skill_name = response_data["data"]["axie"]["parts"][i]["abilities"][0]["name"]
    skill_damage = response_data["data"]["axie"]["parts"][i]["abilities"][0]["attack"]
    skill_type = response_data["data"]["axie"]["parts"][i]["class"]
    skills[skill_name] = skill_damage, skill_type

print(skills)

skill_stats = response_data["data"]["axie"]["stats"]["skill"]
player_axie_type = response_data["data"]["axie"]["class"]

a = [[2,2,2],[2,2,2]]

attack = []
skill_type = []
calculated_attack = []

while not end_turn:
    cards = input("Please enter card name or type 'end' to end turn:\n")

    if cards in skills:
        skill_type.append(skills[cards][1])
        class_multiplier(enemy_class)
        dmg = skills[cards][0] * multiplier
        if skills[cards][1] == player_axie_type:
            added_percent_damage = skills[cards][0] * 0.10
            total_added_damage = added_percent_damage + skills[cards][0] + dmg
            attack.append(round(total_added_damage))
        else:
            a = skills[cards][0] + dmg
            attack.append(a)

        print(skill_type)
        print(attack)

    if cards == "end":
        skill_damage = sum(attack)
        bonus_damage = skill_damage * (skill_stats * 0.55 - 12.25) / 100 * .985

        total_damage = skill_damage + bonus_damage if len(attack) >= 2 else print(skill_damage)

        print(round(total_damage))
        end_turn = True
