import asyncio
from typing import Any
import markdown
from gpt_researcher import GPTResearcher


async def submit_query(researcher: GPTResearcher):
    # Conduct research on the given query
    await researcher.conduct_research()
    # Write the report
    return await researcher.write_report()


def write_html_report(report: Any):
    md = markdown.markdown(str(report))
    with open("mac.html", "w") as f:
        f.write(md)


def write_report(report: Any):
    with open("mac.txt", "w") as f:
        f.write(str(report))


if __name__ == "__main__":
    query = "I have a 2015 iMac i5 running MacOS Monterey and on boot it is hanging with an infinite beach ball loading sign. I have entered recovery mode and on trying to re-install the operating system from the internet, I get a 'pre-flight error' and can progress no further. What are the top 3 possible causes of this problem, ranked from best to worst. Produce your answer with as much technical detail as possible, assuming the user is an experienced software developer on MacOS. If there are solutions or extra logs available from a recovery mode terminal, please suggest these if more information would be useful in diagnosis."

    researcher = GPTResearcher(query=query, report_type="detailed_report")

    report = asyncio.run(submit_query(researcher))
    write_report(report)
    write_html_report(report)
