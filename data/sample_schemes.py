"""
Sample government scheme documents for development and testing.
Each dict represents a scheme with its full text and metadata.
Run `python ingestion/ingest.py` to load these into ChromaDB.
"""

SAMPLE_SCHEMES = [
    {
        "id": "pm_kisan",
        "title": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "content": """
PM-KISAN Scheme – Full Guidelines

Overview:
PM-KISAN provides income support of Rs. 6,000 per year to all landholding farmer families,
paid in three equal instalments of Rs. 2,000 every four months directly into their bank accounts.

Eligibility Criteria:
- The beneficiary must be a farmer family (husband, wife, and minor children).
- The family must own cultivable agricultural land.
- Land size: No upper limit on land size. All landholding farmers are eligible.
- The farmer must be an Indian citizen.
- Must have a valid Aadhaar card.
- Must have a bank account linked to Aadhaar.

Exclusions (NOT eligible):
- Institutional landholders.
- Farmer families where one or more members belong to higher economic status:
  - Former or present holders of constitutional posts.
  - Former or present Ministers/State Ministers/MPs/MLAs/Municipal Mayors/District Panchayat Chairpersons.
  - All serving or retired officers and employees of Central/State Government.
  - All superannuated/retired pensioners with monthly pension >= Rs. 10,000.
  - Those who paid income tax in the last assessment year.
  - Professionals such as Doctors, Engineers, Lawyers, Chartered Accountants registered with Professional bodies.

Required Documents:
1. Aadhaar card (mandatory)
2. Land ownership records / Khatian / ROR (Record of Rights)
3. Bank account details (passbook copy with IFSC code)
4. Mobile number linked to Aadhaar

Application Steps:
Step 1: Visit the official PM-KISAN portal at pmkisan.gov.in
Step 2: Click on 'Farmer Corner' and select 'New Farmer Registration'
Step 3: Enter your Aadhaar number and mobile number for OTP verification
Step 4: Fill in personal details – name, category (General/SC/ST/OBC), bank details
Step 5: Upload land ownership documents
Step 6: Submit the form. Note the registration number for tracking.
Step 7: Your application will be verified by local Patwari/Revenue Officer
Step 8: After verification, funds are transferred directly to your bank account

Helpline: 155261 / 1800115526 (Toll Free)
""",
        "tags": ["farmer", "agriculture", "income support", "rural", "land owner"],
    },
    {
        "id": "ayushman_bharat",
        "title": "Ayushman Bharat – Pradhan Mantri Jan Arogya Yojana (PM-JAY)",
        "ministry": "Ministry of Health and Family Welfare",
        "content": """
Ayushman Bharat PM-JAY – Full Guidelines

Overview:
Ayushman Bharat PM-JAY is the world's largest government-funded health insurance scheme.
It provides health cover of Rs. 5 lakh per family per year for secondary and tertiary care
hospitalisation. Coverage is cashless and paperless at empanelled hospitals.

Eligibility Criteria:
Based on Socio-Economic Caste Census (SECC) 2011 data:

Rural families eligible if they meet ANY ONE of:
- Only one room with kucha walls and kucha roof
- No adult member between 16-59 years
- Female-headed households with no adult male member
- Households with disabled member and no able-bodied adult
- SC/ST households
- Landless households deriving major income from manual casual labour
- Households with BPL (Below Poverty Line) ration card

Urban occupational categories eligible:
- Ragpicker, Beggar, Domestic worker, Street vendor, Construction worker,
  Plumber, Painter, Welder, Security guard, Coolie, Sweeper, Home-based worker,
  Artisan, Handcraft worker, Tailor, Driver, Conductor, Cart/Rickshaw puller,
  Shop worker, Assistant, Helper, Delivery person, Mechanic, Electrician, Repair worker

Family size: No cap — entire family is covered.
Income limit: Based on SECC data, not income.

Required Documents:
1. Aadhaar card OR any government-issued photo ID
2. Ration card (if available)
3. Mobile number
4. The scheme is largely auto-enrolled based on SECC 2011 data — no formal application needed

Application / Enrollment Steps:
Step 1: Check eligibility at beneficiary.nha.gov.in or mera.pmjay.gov.in
Step 2: Enter your mobile number and OTP to verify
Step 3: Search your name using Aadhaar or ration card number
Step 4: If eligible, visit your nearest Common Service Centre (CSC) or empanelled hospital
Step 5: Collect your Ayushman Bharat Golden Card (Ayushman Card) – free of cost
Step 6: Use the Golden Card at any empanelled hospital for cashless treatment

Helpline: 14555 / 1800111565 (Toll Free)
""",
        "tags": ["health", "insurance", "BPL", "SC/ST", "rural", "urban poor", "medical"],
    },
    {
        "id": "pmay_gramin",
        "title": "Pradhan Mantri Awaas Yojana – Gramin (PMAY-G)",
        "ministry": "Ministry of Rural Development",
        "content": """
PMAY-Gramin – Full Guidelines

Overview:
PMAY-G aims to provide pucca houses with basic amenities to homeless households and those
living in dilapidated houses in rural areas. Financial assistance of Rs. 1.20 lakh (plains)
or Rs. 1.30 lakh (hilly/difficult areas) is provided per unit.

Eligibility Criteria:
- Must be a rural household
- Household must be houseless OR living in a kutcha/dilapidated house (0 or 1 room)
- Based on SECC 2011 data, priority to:
  1. Households with no shelter (SC/ST houseless families get priority)
  2. Households with 1 room kutcha house
  3. Families with no adult member (16-59 years)
  4. Female-headed households with no adult male member aged 16-59
  5. Households with a differently-abled member
  6. SC/ST households
  7. Minorities and other categories as per state list

Not eligible:
- Urban area residents (they fall under PMAY-Urban)
- Households already owning a pucca house

Required Documents:
1. Aadhaar card (for all adult members)
2. Job Card (MGNREGS) if available
3. Bank account details
4. SECC 2011 data verification by Gram Sabha
5. Land ownership or allotment documents

Application Steps:
Step 1: Eligibility is primarily determined through SECC 2011 data and Gram Sabha verification
Step 2: Contact your Gram Panchayat (GP) or Block Development Office (BDO)
Step 3: Gram Sabha verifies and approves the beneficiary list
Step 4: Selected beneficiaries are entered on the AwaasSoft MIS portal
Step 5: Geo-tagging and photo upload of house construction at each stage is mandatory
Step 6: Funds are released in three instalments linked to construction progress:
   - 1st instalment: Foundation complete
   - 2nd instalment: Lintel level complete
   - 3rd instalment: Roof slab complete
Step 7: Convergence with MGNREGS (90 days of unskilled labour), Swachh Bharat (toilet),
        and Saubhagya (electricity) schemes

Helpline: 1800116446 (Toll Free)
""",
        "tags": ["housing", "rural", "BPL", "SC/ST", "kutcha house", "shelter"],
    },
    {
        "id": "nsp_scholarship",
        "title": "National Scholarship Portal (NSP) – Central Sector Scheme",
        "ministry": "Ministry of Education",
        "content": """
National Scholarship Portal – Central Sector Scheme of Scholarships

Overview:
The Central Sector Scheme of Scholarships provides financial assistance to meritorious students
from low-income families to meet day-to-day expenses while pursuing higher education.
Amount: Rs. 10,000 per year for undergraduate students; Rs. 20,000 per year for postgraduate.

Eligibility Criteria:
- Indian citizen
- Must have passed Class 12 (10+2) from a recognized board
- Must be among the top 20 percentile of students who passed Class 12 from their board
- Must be enrolled in a regular degree/diploma programme (not correspondence/distance)
- Parental income must NOT exceed Rs. 8 lakh per annum (from all sources)
- Must NOT be availing any other scholarship

Reservation:
- 50% for girls
- 16% for SC students
- 7.5% for ST students

Renewal Conditions:
- Must maintain at least 50% marks in the previous year examination
- Must not have changed the course/institution without prior approval

Required Documents:
1. Aadhaar card
2. Class 12 mark sheet and certificate
3. Bonafide enrollment certificate from college/university
4. Income certificate issued by competent authority (not older than 1 year)
5. Caste certificate (if applying under SC/ST/OBC category)
6. Bank account details (student's own account)
7. Domicile certificate

Application Steps:
Step 1: Visit the National Scholarship Portal at scholarships.gov.in
Step 2: Click on 'New Registration' and complete OTP-based Aadhaar verification
Step 3: Fill in personal details, academic details, and family income details
Step 4: Upload all required documents in specified format (PDF, max 200KB each)
Step 5: Submit the application before the deadline (usually October 31 for fresh applications)
Step 6: Application is verified by the institute nodal officer, then district/state officer
Step 7: Upon approval, scholarship amount is transferred to student's bank account via DBT

Helpline: 0120-6619540
""",
        "tags": ["scholarship", "education", "student", "class 12", "higher education", "income limit"],
    },
    {
        "id": "mudra_loan",
        "title": "Pradhan Mantri MUDRA Yojana (PMMY)",
        "ministry": "Ministry of Finance",
        "content": """
Pradhan Mantri MUDRA Yojana – Full Guidelines

Overview:
MUDRA provides loans to non-corporate, non-farm small/micro enterprises.
Loans are collateral-free. Three categories:
- Shishu: up to Rs. 50,000
- Kishore: Rs. 50,001 to Rs. 5 lakh
- Tarun: Rs. 5,00,001 to Rs. 10 lakh

Eligibility Criteria:
- Any Indian citizen who has a business plan for a non-farm income-generating activity
- Applicable sectors: Manufacturing, Trading, Services, Allied agricultural activities
- Age: 18 years or above
- No minimum income requirement for Shishu loans
- For Kishore and Tarun: Must have an existing business with some track record
- No collateral required (guarantee-free under CGTMSE)

Who can apply:
- Street vendors / hawkers
- Small traders and shopkeepers
- Artisans and craftsmen
- Small manufacturers
- Repair shops, salons, tailors, transporters
- Food processing units
- Self-help groups (SHG)

Not eligible:
- Farm loans (crop loans, land improvement) — those fall under Kisan Credit Card
- Loans above Rs. 10 lakh

Required Documents:
1. Aadhaar card + PAN card (identity proof)
2. Address proof (Voter ID / Utility bill / Passport)
3. Business address proof
4. Business plan / Project report (especially for Kishore and Tarun)
5. Recent 6-month bank statement
6. 2 passport-size photographs
7. Quotation of machinery/equipment to be purchased (if applicable)
8. SC/ST/OBC certificate (if applicable, for priority processing)

Application Steps:
Step 1: Prepare your business plan or project report
Step 2: Visit your nearest Public Sector Bank, Regional Rural Bank, MFI, or NBFC
   OR apply online at udyamimitra.in
Step 3: Fill in the MUDRA loan application form (available at branch or online)
Step 4: Submit documents along with the application
Step 5: Bank conducts due diligence and site visit (for Kishore/Tarun)
Step 6: Upon sanction, loan amount is disbursed to your bank account
Step 7: A MUDRA Card (RuPay debit card) is issued for working capital needs

Helpline: 1800-180-1111 (SIDBI)
""",
        "tags": ["loan", "business", "entrepreneur", "self-employed", "micro enterprise", "startup", "women"],
    },
    {
        "id": "ujjwala_yojana",
        "title": "Pradhan Mantri Ujjwala Yojana (PMUY) 2.0",
        "ministry": "Ministry of Petroleum and Natural Gas",
        "content": """
Pradhan Mantri Ujjwala Yojana 2.0 – Full Guidelines

Overview:
PMUY provides free LPG (cooking gas) connections to women from Below Poverty Line (BPL)
and other deprived households. The scheme covers the cost of security deposit, pressure
regulator, booklet, and first refill.

Eligibility Criteria:
- Must be an adult woman (18 years or above)
- Must belong to any ONE of the following categories:
  - SC/ST households
  - BPL (Below Poverty Line) households
  - Beneficiaries of PMAY (Gramin)
  - Beneficiaries of AAY (Antyodaya Anna Yojana)
  - Tea and Ex-Tea Garden Tribes
  - Forest Dwellers
  - People residing in islands / river islands
  - SECC 2011 listed beneficiaries
  - Any BPL family as listed by state/UT government
- Must not already have an LPG connection in the household
- Must have an Aadhaar card

Required Documents:
1. Aadhaar card (mandatory)
2. Ration card OR any proof of BPL/category status
3. Self-declaration for migrants without address proof (Ujjwala 2.0 relaxation)
4. Bank account details

Application Steps:
Step 1: Visit your nearest LPG distributor of any OMC (IndianOil, HP, Bharat Gas)
Step 2: Ask for the PMUY application form (KYC form)
Step 3: Fill in personal details, Aadhaar number, and bank account details
Step 4: Attach self-declaration for address proof (migrants can use self-declaration)
Step 5: Submit the form at the distributor
Step 6: Your Aadhaar-based KYC is verified online by the OMC
Step 7: Connection is approved and you receive a free connection with first free refill
Step 8: Future refills are subsidised via DBT (Direct Benefit Transfer) to your bank

Helpline: 1906 (LPG Helpline)
""",
        "tags": ["LPG", "cooking gas", "women", "BPL", "SC/ST", "rural", "kitchen"],
    },

    # ── NEW SCHEMES ──────────────────────────────────────────────────────────

    {
        "id": "mgnregs",
        "title": "Mahatma Gandhi National Rural Employment Guarantee Scheme (MGNREGS)",
        "ministry": "Ministry of Rural Development",
        "content": """
MGNREGS – Full Guidelines

Overview:
MGNREGS is a legal guarantee of 100 days of unskilled wage employment per financial year to
every rural household whose adult members are willing to do manual work.
Current wage rate: Rs. 267 per day (varies by state). Payment within 15 days of work.

Eligibility Criteria:
- Must be a resident of a rural area (any village in India)
- Must be an adult (18 years or above)
- Must be willing to do unskilled manual labour
- Belongs to a household (Job Card is issued per household)
- No income restriction – any rural household can apply

Priority groups: Women, SC/ST households, disabled persons, migrant workers.
At least 33% of beneficiaries must be women.

Rights under the Act:
- If work is not provided within 15 days of applying, the applicant is entitled to an
  Unemployment Allowance (1/4 of wage for first 30 days, 1/2 of wage thereafter)

Required Documents:
1. Aadhaar card (for all adult household members)
2. Photograph of the household head
3. Bank or Post Office account details
4. Residence proof (voter ID / ration card)

Application Steps:
Step 1: Visit your Gram Panchayat office and request a Job Card application form
Step 2: Fill in the form with details of all adult household members willing to work
Step 3: Attach Aadhaar copies and one photograph per member
Step 4: Submit at the Gram Panchayat. A Job Card is issued within 15 days
Step 5: When you need work, submit a written/online application to the Gram Panchayat
        requesting employment (minimum 14 days of continuous work)
Step 6: Work is allocated within 15 days; if not, unemployment allowance is paid
Step 7: Wages are credited directly to your bank/post office account within 15 days of
        completing work, based on measured output

Helpline: 1800-111-555 (Toll Free)
""",
        "tags": ["employment", "rural", "manual labour", "job card", "wages", "SC/ST", "women"],
    },
    {
        "id": "sukanya_samriddhi",
        "title": "Sukanya Samriddhi Yojana (SSY)",
        "ministry": "Ministry of Finance",
        "content": """
Sukanya Samriddhi Yojana – Full Guidelines

Overview:
SSY is a small savings scheme for the girl child, offering one of the highest government-
guaranteed interest rates (currently 8.2% p.a., compounded annually). It was launched under
the Beti Bachao Beti Padhao campaign. Tax-free returns under Section 80C of Income Tax Act.

Eligibility Criteria:
- Account can be opened only in the name of a girl child
- Girl child must be below 10 years of age at the time of account opening
- Parent or legal guardian opens the account on behalf of the girl child
- Only one account per girl child is allowed
- Maximum two accounts per family (exception: twins/triplets as second birth)
- Indian citizens only

Deposit Rules:
- Minimum deposit: Rs. 250 per year
- Maximum deposit: Rs. 1.5 lakh per year
- Deposits can be made for 15 years from the date of account opening
- Account matures after 21 years from opening OR when the girl turns 18 and gets married

Partial Withdrawal:
- After the girl turns 18, up to 50% of the balance can be withdrawn for higher education

Required Documents:
1. Birth certificate of the girl child
2. Aadhaar card or proof of identity of the parent/guardian
3. Address proof of the parent/guardian
4. Photograph of the parent/guardian

Application Steps:
Step 1: Visit any Post Office or authorised bank branch (SBI, PNB, Bank of Baroda, etc.)
Step 2: Fill in the SSY account opening form
Step 3: Submit the form with required documents and the initial deposit (minimum Rs. 250)
Step 4: The account is opened and a passbook is issued
Step 5: Make deposits regularly (at least minimum Rs. 250/year) before March 31 each year
Step 6: Track interest and balance via passbook or net banking
Step 7: Maturity amount is paid to the girl child on completion of 21 years or marriage after 18

Helpline: 1800-266-6868 (India Post)
""",
        "tags": ["girl child", "savings", "education", "Beti Bachao", "tax saving", "fixed deposit"],
    },
    {
        "id": "standup_india",
        "title": "Stand-Up India Scheme",
        "ministry": "Ministry of Finance / SIDBI",
        "content": """
Stand-Up India Scheme – Full Guidelines

Overview:
Stand-Up India facilitates bank loans between Rs. 10 lakh and Rs. 1 crore to at least one
SC or ST borrower and at least one woman borrower per bank branch for setting up a greenfield
(new) enterprise in manufacturing, services, agri-allied, or trading sector.

Eligibility Criteria:
- Must be an SC, ST, or woman entrepreneur (18 years or above)
- Loan is for a greenfield project (first-time enterprise; not expansion of existing business)
- The enterprise must be in Manufacturing, Services, Agri-allied, or Trading sector
- In case of non-individual enterprise (partnership/LLP/company), 51% shareholding must be
  held by SC/ST or woman entrepreneur
- Borrower must NOT be in default with any bank or financial institution
- Composite loan (term loan + working capital) between Rs. 10 lakh and Rs. 1 crore

Loan Details:
- Repayment period: up to 7 years
- Moratorium: up to 18 months
- No collateral required (covered under CGFSIL guarantee)

Required Documents:
1. Aadhaar card + PAN card
2. Caste certificate (for SC/ST applicants)
3. Project report / Business plan
4. Address proof of business premises
5. Bank account statements (last 6 months)
6. Photographs
7. Proof of business registration (if already registered)

Application Steps:
Step 1: Register on the Stand-Up India portal at standupmitra.in
Step 2: Fill in personal and business details; get a unique registration number
Step 3: Portal connects you with a bank branch and a handholding agency if needed
Step 4: Prepare your project report with the help of SIDBI/NABARD/DIC
Step 5: Submit loan application at the designated bank branch
Step 6: Bank processes application; sanction letter issued within 4–6 weeks
Step 7: Loan disbursed in tranches linked to project progress

Helpline: 1800-180-1111 (SIDBI)
""",
        "tags": ["loan", "SC/ST", "women", "entrepreneur", "startup", "greenfield", "business"],
    },
    {
        "id": "nps_atal_pension",
        "title": "Atal Pension Yojana (APY)",
        "ministry": "Ministry of Finance / PFRDA",
        "content": """
Atal Pension Yojana – Full Guidelines

Overview:
APY is a government-backed pension scheme focused on workers in the unorganised sector.
Subscribers receive a guaranteed monthly pension of Rs. 1,000 to Rs. 5,000 after age 60,
depending on their contribution amount and age at enrolment.

Eligibility Criteria:
- Must be an Indian citizen
- Age: 18 to 40 years at the time of joining
- Must have a savings bank account (any scheduled bank or post office)
- Must NOT be an income taxpayer (as of May 2022, income taxpayers are excluded)
- Must NOT be a beneficiary of any other statutory social security scheme
  (e.g., EPFO, NPS, ESIC members are excluded)

Pension Amount Options:
- Rs. 1,000/month pension → contribution starts from Rs. 42/month (at age 18)
- Rs. 2,000/month pension → starts from Rs. 84/month (at age 18)
- Rs. 3,000/month pension → starts from Rs. 126/month (at age 18)
- Rs. 4,000/month pension → starts from Rs. 168/month (at age 18)
- Rs. 5,000/month pension → starts from Rs. 210/month (at age 18)
(Contributions increase with joining age)

On subscriber's death, spouse receives same pension; on spouse's death, nominee receives corpus.

Required Documents:
1. Aadhaar card
2. Savings bank account details
3. Mobile number linked to bank account

Application Steps:
Step 1: Visit your bank branch or post office and ask for the APY enrollment form
   OR apply online through your bank's net banking portal under the 'Social Security' section
Step 2: Fill in the form with personal details, nominee name, and choose pension amount
Step 3: Provide your Aadhaar number and bank account details for auto-debit setup
Step 4: Sign and submit. Bank sets up the monthly auto-debit
Step 5: You receive a PRAN (Permanent Retirement Account Number) via SMS/post
Step 6: Track your account at npscra.nsdl.co.in using your PRAN
Step 7: At age 60, approach bank for pension disbursement

Helpline: 1800-110-069 (PFRDA Toll Free)
""",
        "tags": ["pension", "unorganised sector", "retirement", "savings", "senior citizen", "low income"],
    },
    {
        "id": "pmfby",
        "title": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "content": """
Pradhan Mantri Fasal Bima Yojana – Full Guidelines

Overview:
PMFBY provides comprehensive crop insurance to farmers against crop loss/damage due to
natural calamities (flood, drought, cyclone, hailstorm, pest/disease).
It covers all food crops, oilseeds, and annual commercial/horticultural crops.

Premium rates (farmer's share):
- Kharif crops: 2% of sum insured
- Rabi crops: 1.5% of sum insured
- Annual commercial/horticultural crops: 5% of sum insured
- Rest of the premium is paid as subsidy by Central and State Governments

Eligibility Criteria:
- All farmers (loanee and non-loanee) growing notified crops in notified areas
- Loanee farmers: Compulsorily covered (premium auto-deducted from crop loan)
- Non-loanee farmers: Voluntary enrollment
- Tenant/sharecropper farmers are also eligible (with an agreement letter from land owner)
- Must have a valid Aadhaar card

Risks Covered:
- Prevented Sowing/Planting due to deficit rainfall or adverse seasonal conditions
- Standing crop losses (from sowing to harvesting)
- Post-harvest losses (up to 14 days after harvesting)
- Localised calamities (hailstorm, landslide, inundation)

Required Documents:
1. Aadhaar card
2. Land ownership / tenancy documents
3. Sown crop declaration (crop, sown area, sowing date)
4. Bank account details

Application Steps:
Step 1: Contact your nearest bank branch, CSC, or insurance company agent
   OR apply online at pmfby.gov.in
Step 2: Submit crop sowing details and land records before the cutoff date
   (Kharif: July 31; Rabi: December 31 – may vary by state)
Step 3: Pay the applicable premium; loanee farmers' premium is auto-deducted
Step 4: Receive policy document / insurance number
Step 5: In case of crop loss, notify the insurer/bank/agriculture department within 72 hours
Step 6: Survey and crop-cutting experiments (CCE) determine loss assessment
Step 7: Claim amount is transferred directly to bank account via DBT

Helpline: 1800-200-7710 (Toll Free)
""",
        "tags": ["crop insurance", "farmer", "agriculture", "kharif", "rabi", "natural disaster", "flood", "drought"],
    },
    {
        "id": "pmgsy",
        "title": "Pradhan Mantri Gram Sadak Yojana (PMGSY)",
        "ministry": "Ministry of Rural Development",
        "content": """
Pradhan Mantri Gram Sadak Yojana – Full Guidelines

Overview:
PMGSY aims to provide all-weather road connectivity to unconnected rural habitations.
Under PMGSY-III, it also upgrades existing rural roads to improve road network efficiency.

Eligibility (for habitation to receive a road):
- Unconnected habitations with a population of 500 or more (250 in hilly/tribal/desert/LWE areas)
- Identified in the Core Network of the district
- Must not already have an all-weather road

Who benefits: Entire community of the habitation, especially women, farmers, students, patients.

How citizens can raise a demand:
- Any citizen or Gram Panchayat can submit a request to the District Collector or Block Development Officer
- Request is reviewed and included in the district's Comprehensive Road Plan (RCPLWSS)

Required Documents (for Gram Panchayat to submit demand):
1. Resolution passed by Gram Sabha
2. Population census data of the habitation
3. Details of existing connectivity (or lack thereof)
4. GPS coordinates of the habitation

Steps to Request/Track a Road under PMGSY:
Step 1: Gram Panchayat passes a resolution and submits demand to the District Panchayat / Block Office
Step 2: District prepares a Detailed Project Report (DPR) if habitation is eligible
Step 3: DPR is approved at the state level and uploaded to the OMMAS portal
Step 4: Tender is floated; construction agency is selected
Step 5: Construction begins; quality is monitored by National Quality Monitors (NQMs)
Step 6: Citizens can track road construction status at omms.nic.in
Step 7: Completed roads are handed over to the Gram Panchayat for maintenance

Helpline: grievances can be raised at pgportal.gov.in
""",
        "tags": ["road", "rural connectivity", "village", "infrastructure", "gram panchayat", "tribal", "hilly"],
    },
    {
        "id": "e_shram",
        "title": "e-Shram Portal – Unorganised Workers Registration",
        "ministry": "Ministry of Labour and Employment",
        "content": """
e-Shram Portal – Full Guidelines

Overview:
e-Shram is a national database of unorganised workers. Registered workers receive an e-Shram
card (UAN – Universal Account Number) which serves as a universal identity for accessing
social security benefits. Registered workers also get accidental insurance cover of Rs. 2 lakh
under PMSBY (Pradhan Mantri Suraksha Bima Yojana) for the first year.

Eligibility Criteria:
- Must be an unorganised worker (not a member of EPFO or ESIC)
- Age: 16 to 59 years
- Must be working in the unorganised sector such as:
  - Construction workers, Migrant workers, Domestic workers
  - Street vendors, Agricultural labourers, Fishermen
  - Auto/Taxi drivers, Beedi workers, Handloom workers
  - Leather & tannery workers, Mid-day meal workers, Rickshaw pullers
  - Sanitation workers, Cobblers, Washermen (Dhobi), and more
- Must NOT be an income tax payer
- Must have an Aadhaar card linked to a mobile number

Benefits of Registration:
- Unique UAN (Universal Account Number) card
- Rs. 2 lakh accidental insurance (free for first year via PMSBY)
- Priority access to future government social security schemes
- Portability of benefits even after migrating to another state

Required Documents:
1. Aadhaar card (mobile number must be linked to Aadhaar for OTP)
2. Bank account details (for DBT of future benefits)

Registration Steps:
Step 1: Visit eshram.gov.in OR go to the nearest CSC (Common Service Centre)
Step 2: Enter your Aadhaar-linked mobile number and verify via OTP
Step 3: Your details are auto-fetched from UIDAI using Aadhaar
Step 4: Select your occupation/work category and provide bank account details
Step 5: Submit the form – your e-Shram card with a 12-digit UAN is generated instantly
Step 6: Download or print your e-Shram card
Step 7: Show your e-Shram card to access linked welfare schemes

Helpline: 14434 (Toll Free)
""",
        "tags": ["unorganised worker", "labour", "construction", "migrant", "domestic worker", "insurance", "UAN"],
    },
    {
        "id": "pmvvy",
        "title": "Pradhan Mantri Vaya Vandana Yojana (PMVVY)",
        "ministry": "Ministry of Finance / LIC of India",
        "content": """
Pradhan Mantri Vaya Vandana Yojana – Full Guidelines

Overview:
PMVVY is a pension scheme exclusively for senior citizens (60+), operated through LIC of India.
It provides a guaranteed pension at a fixed rate of 7.4% p.a. for 10 years,
payable monthly, quarterly, half-yearly, or yearly.

Eligibility Criteria:
- Must be a senior citizen: 60 years of age or above (no upper age limit)
- Must be an Indian citizen (NRIs not eligible)
- Can be purchased by self or through bank, insurance agent, LIC branch

Investment Limits:
- Minimum investment: Rs. 1.56 lakh (for Rs. 1,000/month pension)
- Maximum investment: Rs. 15 lakh per senior citizen (for Rs. 9,250/month pension)
- Pension mode options: Monthly / Quarterly / Half-yearly / Yearly

On maturity (after 10 years): Purchase price is returned to the pensioner.
On premature exit (after 3 years for critical illness): 98% of purchase price returned.
Loan facility: Available after 3 years (up to 75% of purchase price).

Required Documents:
1. Age proof (Aadhaar / Birth certificate / Passport / PAN card)
2. Address proof
3. Bank account details for pension credit
4. Photograph

Application Steps:
Step 1: Visit any LIC branch across India OR apply online at licindia.in
Step 2: Fill in the PMVVY proposal form (Form 700)
Step 3: Submit KYC documents – age proof, address proof, photographs
Step 4: Pay the lump-sum purchase price (single premium) by cheque/DD/NEFT
Step 5: Policy is issued; pension disbursement starts from next month/quarter/half-year/year
Step 6: Pension is directly credited to your bank account on due dates
Step 7: On maturity (10 years), purchase price is automatically returned to bank account

Helpline: 022-68276827 (LIC)
""",
        "tags": ["senior citizen", "pension", "retirement", "LIC", "elderly", "fixed income", "60+"],
    },
    {
        "id": "bbbp_pc_pndt",
        "title": "Beti Bachao Beti Padhao (BBBP) Scheme",
        "ministry": "Ministry of Women and Child Development",
        "content": """
Beti Bachao Beti Padhao – Full Guidelines

Overview:
BBBP is a social campaign launched to address the declining Child Sex Ratio (CSR) and promote
the welfare, education, and empowerment of the girl child. It also covers strict enforcement
of the PC&PNDT Act (Pre-Conception and Pre-Natal Diagnostic Techniques).

Objectives:
1. Prevent gender-biased sex selective elimination
2. Ensure survival and protection of the girl child
3. Ensure education and participation of the girl child

Who Benefits:
- Girl children (0-18 years)
- Pregnant women and mothers
- Communities in districts with low Child Sex Ratio (CSR < 918 girls per 1000 boys)

Key Interventions for Citizens:
A) Conditional Cash Transfer for Girl Child (varies by state):
   - Many states run linked schemes (e.g., Dhanlakshmi, Kanya Sumangala Yojana, Ladli Laxmi)
   - Incentives for girl's birth registration, immunisation, school enrolment, and education

B) Awareness Campaigns:
   - Community mobilisation, street plays (Nukkad Nataks), school programmes

Eligibility for State-Linked Cash Transfer Schemes (general criteria):
- The girl child must be born in a government hospital or registered private hospital
- Family must be from economically weaker sections (income varies by state)
- Girl child must not have a registered previous girl sibling in some states
- Birth must be registered within 1 year

Required Documents:
1. Birth certificate of the girl child
2. Aadhaar card of parents
3. BPL/income certificate
4. Bank account in the name of the girl child or mother

Application Steps:
Step 1: Register birth of the girl child at the nearest PHC (Primary Health Centre) or municipality
Step 2: Contact your Anganwadi worker or CDPO (Child Development Project Officer) for cash transfer linkage
Step 3: Submit the application with required documents
Step 4: Verification is done by the district-level committee
Step 5: Benefits are transferred to the girl child's / mother's bank account at defined milestones
         (birth, immunisation, Class 1 enrolment, Class 6 enrolment, Class 9 enrolment, Class 12 completion)
Step 6: For education support, ensure girl child remains enrolled in school each year

Helpline: 181 (Women Helpline)
""",
        "tags": ["girl child", "women", "education", "child welfare", "BPL", "gender", "birth", "school"],
    },
]
