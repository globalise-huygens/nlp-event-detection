



spelling1 = ['HavingInternalState', 'HavingInternalState-']
spelling2 = ['TakingUnderControl', 'TakingSomeoneUnderControl']


x = 'HavingInternalState'
if x in spelling1:
    print('yes')

translocation_events = ['TransLocation', 'Transportation', 'Leaving', 'Arriving', 'Voyage', 'Translocation']

def taxonomic_resolve(annos, possible_classes, resolution):
    with_resolutions = []
    for item in annos:
        print(item)
        if type(item) == str:
            with_resolutions.append(item)
        else:
            #new = (s if s != 'TakingSomeoneUnderControl' else "TakingUnderControl" for s in item)
            #print(new)
            counted = count(item)
            keys = []
            for key, value in counted.items():
                keys.append(key)
                i=0
                for key in keys:
                    if key in possible_classes:
                        i+=1

                if i >= 3:
                    with_resolutions.append(resolution)
                else:
                    with_resolutions.append(item)
    return(with_resolutions)


result = taxonomic_resolve(first_resolve_class, translocation_events, 'Translocation')
print(result)


i_class=0
i_noneclass = 0
i_unresolved = 0
for item in result:
    if type(item) == str and item != '0':
        i_class += 1
        print(item)
    if type(item) == str and item == '0':
        i_noneclass += 1
    if type(item) != str:
        i_unresolved +=1

print()
print('Second resolve step (merging classes on taxonomic level for Translocation events) resulted in a total resolution of ', i_class)
print('not resolved: ', i_unresolved)


translocation_events = ['TransLocation', 'Transportation', 'Leaving', 'Arriving', 'Voyage', 'Translocation']
possession_events = ['Buying', 'Selling', 'Getting', 'Giving', 'LosingPossession', 'FinancialTransaction', 'Trade',
                         'ChangeOfPossession']
violentcontest_events = ['ViolentContest', 'Attacking', 'Besieging', 'Invasion', 'Killing']
social_interact_conflict_events = ['StartingAWar', 'EndingAWar', 'EndingAConflict', 'StartingAConflict']
unrest_events = ['Mutiny', 'Riot', 'PoliticalRevolution', 'Uprising']
relationship_events = ['BeginningARelationship', 'RelationshipChange', 'AlteringARelationship',
                           'EndingARelationship']
scalar_events = ['ScalarChange', 'Decreasing', 'Increasing', 'QuantityChange']


stateplus_events = ['Repairing', 'Healing']
statemin_events = ['Damaging', 'FallingIll']
translocation_static = ['BeingAtAPlace']
possession_static = ['HavingInPossession']
conflict_static = ['BeingInConflict', 'War']
unrest_static = ['Unrest']
relationship_static = ['BeingInARelationship']
internalmin_static = ['HavingInternalState-', 'HavingInternalState']
internalplus_static = ['HavingInternalState+']