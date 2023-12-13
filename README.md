# Studying-the-Performance-of-IPv6-and-IPv4

## Overview
This project aimed to evaluate and compare the performance of IPv4 and IPv6 connections across 4G networks provided by different ISPs (Jio and Airtel) while analyzing the geolocation data derived from the websites' IP addresses. The study involved various tests including ping, traceroute, and page retrieval times for a selected group of websites to assess network efficiency and the impact of different Internet protocols.

## Problem Statement
The project's aim was to:
- Compare IPv4 and IPv6 connections' performance through ping tests and traceroute analysis.
- Assess website retrieval times using Wget for both IPv4 and IPv6.
- Correlate geolocation data derived from the IP addresses with connectivity performance metrics.

## Methodology
### Websites Selection
- Curated a diverse list of websites ensuring support for both IPv4 and IPv6.
### Network and Tools
- Utilized 4G networks from Jio and Airtel ISPs via mobile hotspot.
- Employed tools like ping, traceroute, and Wget for data collection.
### Data Collection
- Conducted automated ping tests on selected websites using both IPv4 and IPv6 addresses.
- Tracked geolocation data based on IP addresses, hops data using traceroute, and website content retrieval times.
- Automated data collection, analysis, and graph generation using Python and shell scripts.

## Data Collection Period
- Ping/traceroute data: 11th to 17th November 2023
- Wget data: 26th November to 2nd December 2023

## Results
### Key Graphs and Findings
- **RTT Comparison**: Jio showed better performance than Airtel for both IPv4 and IPv6, with India exhibiting the best results due to proximity.
- **Hops Comparison**: Jio displayed fewer hops than Airtel, maintaining its superiority.
- **Page Retrieval Times**: Minimal difference observed between IPv4 and IPv6 in fetching full webpages.
- **Country-wise Wget Speeds**: Proximity to India favored faster data retrieval; notable case of Australia performing exceptionally well.
- **Other Insights**: 
    - Geolocation data for IPv6 was challenging to obtain.
    - Airtel encountered more connection refusals with IPv6 compared to Jio.
    - Overall, IPv6 performed better for Jio across metrics, while its performance varied for Airtel.

### Interesting Findings
- Geolocation data for IPv6 was scarce and not well-maintained in databases.
- Airtel faced more connection refusals with IPv6 than Jio.
- IPv6 performed better consistently for Jio but had varying results with Airtel.
- Minimal transfer rate gains observed between IPv4 and IPv6.

## Contributions
- Akshat Tilak: Data collection and analysis
- Jahanvi Bakshi: Data collection and report generation
- Yogesh Kaushik: Scripting and data analysis
- Shubham Sharma: Data collection and analysis
