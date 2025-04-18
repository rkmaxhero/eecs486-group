import os
from collections import Counter
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# https://www.raceforward.org/sites/default/files/DTIW_Stylebook.pdf
# chatgpt
STYLE_GUIDE_REPLACEMENTS = {
    "illegal immigrant": "unauthorized immigrant",
    "illegal immigrants": "unauthorized immigrants",
    "illegal alien": "undocumented immigrant",
    "illegal aliens": "undocumented immigrants",
    "illegals": "immigrants without papers",
    "an illegal": "an immigrant without legal status",
    "illegal person": "person without legal status",
    "illegal people": "people without legal status",
    "illegal status": "unauthorized status",
    "illegal entry": "unauthorized entry",
    "illegal border crossing": "unauthorized border crossing",
    "illegal worker": "undocumented worker",
    "illegal family": "undocumented family",
    "illegal parents": "undocumented parents",
    "illegal child": "child of undocumented immigrants",
    "illegal national": "noncitizen without legal status",
    "illegal population": "undocumented population",
    "illegal communities": "undocumented communities",
    "illegal presence": "unauthorized presence",
    "illegal residence": "unauthorized residence",
    "illegal occupation": "unauthorized stay",
    "illegal resident": "unauthorized resident",
    "illegal crossing": "unauthorized crossing",
    "illegal migration": "unauthorized migration",
    "illegal nationals": "noncitizens without documentation",
    "illegal birth": "citizenship through undocumented parents",
    "anchor baby": "citizen child of undocumented immigrants",
    "anchor babies": "citizen children of undocumented immigrants",
    "undocumented alien": "undocumented immigrant",
    "unlawful immigrant": "unauthorized immigrant",
    "unlawful aliens": "undocumented immigrants",
    "unlawful entry": "unauthorized entry",
    "alien": "immigrant",
    "aliens": "immigrants",
    "criminal alien": "immigrant with a criminal conviction",
    "deportable alien": "removable noncitizen",
    "overstayer": "person who overstayed their visa",
    "visa violator": "person who overstayed their visa",
    "assimilation": "integration",
    "low-skilled immigrant": "immigrant with limited formal training",
    "non-citizen": "immigrant",
    "noncitizen": "immigrant",
    "birth tourism": "giving birth in the U.S. to secure citizenship for one’s child",

    # Sensationalist framing
    "flood of immigrants": "increase in immigration",
    "wave of immigrants": "rise in immigration",
    "invasion": "increase in migration",
    "invaders": "migrants",
    "stampede": "surge in immigration",
    "onslaught": "arrival of new immigrants",
    "mass illegal immigration": "large-scale unauthorized immigration",
    "illegals flooding in": "immigrants arriving in large numbers",
    "immigrant surge": "increased migration flow",
    "overrun by immigrants": "seeing increased immigration",
    "swarming the border": "crossing the border",
    "border crisis": "increase in border crossings",

    # Criminalizing language
    "breaking the law": "violating immigration rules",
    "sneaking across the border": "crossing the border without authorization",
    "border jumper": "person who crossed the border without authorization",
    "illegal behavior": "unauthorized action",
    "law-breaking immigrant": "immigrant without status",
    "criminal border crosser": "person crossing without authorization",
    "illegally entered": "entered without authorization",
    "illegal conduct": "unauthorized immigration action",
    "immigration offender": "person with an immigration violation",
    "undocumented criminals": "people with undocumented status and criminal records",
    "immigrant criminals": "immigrants with criminal records",

    # Dehumanizing phrases
    "the illegals": "people without documentation",
    "these illegals": "these undocumented individuals",
    "illegals coming in": "undocumented people arriving",
    "those people": "people",
    "foreigners": "people from other countries",
    "outsiders": "immigrants",
    "aliens": "immigrants",
    "them": "people from immigrant communities",

    # Legal process reframing
    "amnesty": "legalization process",
    "catch and release": "release pending immigration hearing",
    "chain migration": "family-based immigration",
    "loophole": "policy gap",
    "gaming the system": "seeking lawful immigration options",
    "illegal loophole": "legal ambiguity",
    "deferred deportation": "protection from removal",
    "anchor baby loophole": "birthright citizenship",
    "illegal protections": "legal protections for undocumented individuals",

    # Coded racialized language
    "third world immigrants": "immigrants from developing countries",
    "low quality immigrants": "immigrants from economically disadvantaged regions",
    "non-white immigrants": "immigrants of color",
    "illegal Mexicans": "undocumented Mexican immigrants",
    "illegal Hispanics": "undocumented Latinx immigrants",

    # Immigration policy euphemisms
    "zero tolerance": "strict enforcement policy",
    "removal": "deportation",
    "deportation force": "immigration enforcement team",
    "mass deportation": "large-scale deportation",
    "round-up": "large-scale detention",
    "raid": "immigration enforcement action",
    "ICE crackdown": "increased ICE enforcement",
    "family separation": "removal of children from undocumented parents",

    # Misc
    "native-born": "U.S.-born",
    "job-stealing immigrant": "immigrant seeking employment",
    "stealing jobs": "competing for jobs",
    "drain on the system": "use of public services",
    "tax burden": "recipient of government assistance",
}


#count style guide phrase occurrences in article
def count_style_guide_replacements(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()
    phrase_count = {phrase: text.count(phrase) for phrase in STYLE_GUIDE_REPLACEMENTS.keys()}
    return phrase_count

def read_stopwords(file_path):
    stopwords = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            stopwords.add(line.strip().lower())
    return stopwords

def get_top_words_by_source(directory, stopwords, source_prefix, n=20):
    word_counter = Counter()

    for filename in os.listdir(directory):
        if filename.startswith(source_prefix):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read().lower()
                    tokens = nltk.word_tokenize(text)
                    filtered_tokens = [word for word in tokens if word.isalpha() and word not in stopwords]
                    word_counter.update(filtered_tokens)

    return word_counter.most_common(n)

def analyze_connotation(word, sia):
    score = sia.polarity_scores(word)
    if score['compound'] >= 0.05:
        return 'positive'
    elif score['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'

# analyze sentences in each article
def analyze_article_bias(file_path, sia, style_guide_counts):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    total = len(lines)
    pos_count = 0
    neg_count = 0
    neutral_count = 0

    for line in lines:
        score = sia.polarity_scores(line.strip())
        compound = score['compound']

        if compound >= 0.05:
            pos_count += 1
        elif compound <= -0.05:
            neg_count += 1
        else:
            neutral_count += 1

    pscore = pos_count / total if total > 0 else 0
    nscore = neg_count / total if total > 0 else 0
    neutral_score = neutral_count / total if total > 0 else 0

    #apply penalty for style guide phrases
    for phrase, count in style_guide_counts.items():
        if count > 0:
            nscore += count * 0.001
    
    nscore = round(nscore, 3)

    if abs(pscore - nscore) < 0.05:
        final = 'neutral'
    elif pscore > nscore:
        final = 'positive'
    else:
        final = 'negative'

    return pos_count, neg_count, neutral_count, round(pscore, 3), round(nscore,3), round(neutral_score,3), final

def process_bias_analysis(source_prefix, parsed_articles_dir, output_dir, sia, mode):
    # the filename depends on the mode, if its training or testing

    if mode == "training":
        output_path = os.path.join(output_dir, f"{source_prefix}_bias_analysis_initial.txt")
    elif mode == "testing":
        output_path = os.path.join(output_dir, f"{source_prefix}_bias_analysis_final.txt")
    # output_path = os.path.join(output_dir, f"{source_prefix}_bias_analysis.txt")
    with open(output_path, 'w', encoding='utf-8') as out_file:
        out_file.write("filename\tpos\tneg\tneu\tpscore\tnscore\tneuscore\tfinalscore\n")

        for filename in sorted(os.listdir(parsed_articles_dir)):
            if filename.startswith(source_prefix):
                file_path = os.path.join(parsed_articles_dir, filename)
                if os.path.isfile(file_path):
                    style_guide_counts = count_style_guide_replacements(file_path)

                    pos, neg, neutral, pscore, nscore, neuscore, final = analyze_article_bias(file_path, sia, style_guide_counts)
                    out_file.write(f"{filename}\t{pos}\t{neg}\t{neutral}\t{pscore}\t{nscore}\t{neuscore}\t{final}\n")
    
    print(f"Bias analysis saved: {output_path}")

def process_source(source_prefix, stopwords_path, parsed_articles_dir, output_dir, mode):
    print(f"Processing source: {source_prefix}")

    os.makedirs(output_dir, exist_ok=True)

    stopwords = read_stopwords(stopwords_path)
    sia = SentimentIntensityAnalyzer()

    # Word frequency part
    top_words = get_top_words_by_source(parsed_articles_dir, stopwords, source_prefix, n=20)
    top_words_path = os.path.join(output_dir, f"{source_prefix}_top_words.txt")
    with open(top_words_path, 'w', encoding='utf-8') as out_file:
        out_file.write(f"Top 20 words for source '{source_prefix}':\n\n")
        for word, freq in top_words:
            connotation = analyze_connotation(word, sia)
            out_file.write(f"{word}: {freq}, connotation: {connotation}\n")

    print(f"Top words saved: {top_words_path}")

    # Run the new bias analysis
    process_bias_analysis(source_prefix, parsed_articles_dir, output_dir, sia, mode)

def main():
    src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    stopwords_path = os.path.join(src_dir, 'library', 'stopwords.txt')
    training_articles_dir = os.path.join(src_dir, 'parsed_articles')
    testing_articles_dir = os.path.join(src_dir, 'parsed_articles_neutralized')
    output_dir = os.path.join(src_dir, 'training_output')

    for source in ['cnn', 'fox']:
        process_source(source, stopwords_path, training_articles_dir, output_dir, "training")
        process_source(source, stopwords_path, testing_articles_dir, output_dir, "testing")

if __name__ == "__main__":
    main()
