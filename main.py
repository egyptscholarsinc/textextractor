import stanza
import os
import textract
import sys

if len(sys.argv) == 1:
	print("Command: python main.py <archive containing resumes>")
	quit()

stanza.download('en')
output = list()
dir = sys.argv[1]
output_file = open("resumes.tsv", "w")
problem = list()
problem_file = open("problem-entries.txt", "w")

count = 0
total = len(os.listdir(dir))
output_file.write(f'Filename\tName\tResume\n')

for file in os.listdir(dir):
	text = ""
	try:
		text = textract.process(f'{dir}/{file}')
		text = text.decode('utf-8')
	except:
		problem.append(file)
	
	if text != "":
		count += 1
		nlp = stanza.Pipeline(
			lang='en', processors='tokenize,ner', verbose=False)

		text = text.replace('\t',' ')
		text = text.replace('\r','\n')
		text = text.replace('\uf0b7',' ')
		text = ' '.join(text.split())

		subset = text.split('\n')[:10]
		subset = '. '.join(subset)
		text = text.replace('\n',' ')

		doc = nlp(subset)
		entities = list()
		name = ""
		for ent in doc.ents:
			if ent.type == 'PERSON':
				name = ent.text
				break
		
		output_file.write(f"{file}\t{name}\t{text}\n")
		print(f'{file} - {count}/{total}')

output_file.close()

for line in problem:
	problem_file.write(line)
	problem_file.write("\n")

problem_file.close()

print("Comlpeted Extraction")