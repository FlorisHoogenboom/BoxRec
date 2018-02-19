from boxrec.services import FightServiceFactory

fight_service = FightServiceFactory.make_service()

fight = fight_service.find_by_id(763615, 2220538)

print(fight.fight_id)
print(fight.boxer_left.name)
print(fight.boxer_right.name)