"""
Module for parsing school names
"""

from us import states


def update_school_name(school_name):
    """
    Updates a school name from its common abbreviation to its more formalized version.
    Also prunes parentheses.

    Parameters
    ----------
    school_name: str

    Returns
    -------
    str
    """
    if school_name[-1] == ")" and school_name[-4] == "(":
        school_name = school_name[:-5]
    elif school_name[-1] == ")" and school_name[-3] == "(":
        school_name = school_name[:-4]
    if school_name in SPECIAL_CASES:
        school_name = SPECIAL_CASES[school_name]
    elif school_name in STATES:
        school_name = f"University of {school_name}"
    return school_name


FORMAL_TO_ABBREV = {
    "University at Albany, SUNY": "Albany",
    "University of Maryland, Baltimore County": "UMBC",
    "University of Central Florida": "UCF",
    "Southern Methodist University": "SMU",
    "University of Maryland, College Park": "Maryland",
    "University of North Carolina at Chapel Hill": "UNC",
    "Georgia Institute of Technology": "Georgia Tech",
    "North Carolina State University": "NC State",
    "University of North Carolina at Asheville": "UNC Asheville",
    "Virginia Polytechnic Institute and State University": "Virginia Tech",
    "University of California, Berkeley": "Cal",
    "University of Connecticut": "UConn",
    "University of Pittsburgh": "Pitt",
    "University of California, Los Angeles": "UCLA",
    "University of Illinois Urbana-Champaign": "Illinois",
    "University of Pennsylvania": "Penn",
    "University of Wisconsin-Madison": "Wisconsin",
    "Indiana University Bloomington": "Indiana",
    "Austin Peay State University": "Austin Peay",
    "Florida Gulf Coast University": "FGCU",
    "Boston College": "Boston College",
    "University of Massachusetts Amherst": "UMass",
    "Virginia Commonwealth University": "VCU",
    "Rutgers University-New Brunswick": "Rutgers",
    "University of Texas at Austin": "Texas",
    "Texas Christian University": "TCU",
    "California Polytechnic State University": "Cal Poly",
    "California State University, Bakersfield": "CSUB",
    "California State University, Fullerton": "CSUF",
    "California State University, Northridge": "CSUN",
    "University of California, Davis": "UC Davis",
    "University of California, Irvine": "UC Irvine",
    "University of California, San Diego": "UCSD",
    "University of California, Santa Barbara": "UCSB",
    "College of Charleston": "Charleston",
    "North Carolina Agricultural and Technical State University": "NC A&T",
    "University of North Carolina at Wilmington": "UNC Wilmington",
    "University of North Carolina at Charlotte": "UNC Charlotte",
    "Florida Atlantic University": "FAU",
    "Louisiana Tech University": "LA Tech",
    "University of Texas at El Paso": "UTEP",
    "University of Texas at San Antonio": "UTSA",
    "University of Wisconsin-Milwaukee": "Milwaukee",
    "University of Wisconsin-Green Bay": "UW-Green Bay",
    "University at Buffalo": "Buffalo",
    "Colorado State University": "CSU",
    "San Diego State University": "SDSU",
    "Pennsylvania State University": "Penn State",
    "University of Southern California": "USC",
    "Saint Mary's College of California": "St. Mary's",
    "University of Nevada, Reno": "Nevada",
    "University of Louisiana at Lafayette": "Louisiana-Lafayette",
    "Texas A&M University-Corpus Christi": "AMCC",
    "New Mexico State University": "NM State",
    "Louisiana State University": "LSU",
    "University of Alabama at Birmingham": "UAB",
    "University of Tennessee at Chattanooga": "Chattanooga",
    "Loyola University Chicago": "Loyola Chicago",
    "University of Texas at Arlington": "UT Arlington",
    "University of Hawaii at Manoa": "Hawaii",
    "University of Nevada, Las Vegas": "UNLV",
    "Alabama Agricultural and Mechanical University": "Alabama A&M",
    "New Jersey Institute of Technology": "NJIT",
    "Brigham Young University": "BYU",
    "Brigham Young": "BYU",
}
SPECIAL_CASES = {
    "UConn": "University of Connecticut",
    "Illinois": "University of Illinois Urbana-Champaign",
    "Texas": "University of Texas at Austin",
}
STATES = [str(s) for s in states.STATES]
