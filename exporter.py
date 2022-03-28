import csv

def save_to_file(jobs) :
  file = open('jobkorea.csv', mode = 'w', encoding='utf-8-sig')
  writer = csv.writer(file)
  writer.writerow(['title', 'company', 'location', 'apply_link'])
  for job in jobs :
    writer.writerow(list(job.values()))
  return 