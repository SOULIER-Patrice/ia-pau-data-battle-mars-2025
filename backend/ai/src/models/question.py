def generate_mcq(questions: str) -> dict:
    return {'question': 'An applicant files an international application with 20 pages of description, 5 claims, and figures. The application enters the European phase 19 months after the filing date (no priority claimed). If the applicant wants to make amendments before receiving the search report, which statement is correct?', 'options': ['A. Amendments can be made only in the international phase.', 'B. Amendments can be made both in the international and European phases, provided they are consistent with the original filing date.', 'C. No amendments can be made until after receiving the search report.', 'D. Amendments can be made at any time before the grant of the patent.']}


def generate_open(questions : str) -> str:
    response = """A Japanese company has filed a European patent application in Japanese, which is not an official EPO language. The application was submitted on March 15, 2023.

    a) What languages can be used for filing this European patent application?

    b) When must the translation into an admissible non-EPO language be submitted to the EPO?

    c) If the company fails to file the translation within the required timeframe, what will happen according to Rule 58 and Rule 112(1)?
    """
    return response
