sero = read.csv('sero.csv')

newsero = sero %>% group_by(location, date) %>% summarise(sero_participants = sum(participants), avg_sero = weighted.mean(x = seroprevalence, w = participants))

write.csv(x = newsero, file="new_sero.csv", row.names = FALSE)

