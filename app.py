import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Analiză Economică PV + Storage cu profil orar")

# Input utilizator
consum_orar = st.slider('Consum mediu orar al fabricii (MWh)', 0.0, 5.0, 1.0)
putere_pv = st.slider('Putere PV (MWp)', 0.0, 15.0, 2.0)
capacitate_baterie = st.slider('Capacitate baterie (MWh)', 0.0, 100.0, 10.0)

# Profil orar simplificat
ore_an = 8760
ore_zi = 24
consum_anual = consum_orar * ore_an
productie_orara_pv = np.zeros(ore_zi)
productie_orara_pv[8:18] = putere_pv / (18-8)  # Producție PV între orele 8-18

productie_anuala_pv = np.tile(productie_orara_pv, 365)
consum_orar_vector = np.full(ore_an, consum_orar)

# Simulare orară
baterie = capacitate_baterie
soc_baterie = 0
injectie_retea = 0
autoconsum_total = 0
consum_retea = 0

for ora in range(ore_an):
    prod_pv = productie_anuala_pv[ora]
    cons = consum_orar_vector[ora]

    exces_prod = prod_pv - cons

    if exces_prod >= 0:
        autoconsum_total += cons
        if soc_baterie < baterie:
            incarcare = min(exces_prod, baterie - soc_baterie)
            soc_baterie += incarcare
            injectie_retea += exces_prod - incarcare
        else:
            injectie_retea += exces_prod
    else:
        necesar = abs(exces_prod)
        if soc_baterie >= necesar:
            soc_baterie -= necesar
            autoconsum_total += cons
        else:
            autoconsum_total += soc_baterie
            consum_retea += necesar - soc_baterie
            soc_baterie = 0

# Parametri economici
cost_pv_kwp = 800
cost_baterie_kwh = 400
pret_autoconsum = 160
pret_injectare = 55
pret_retea = 160

valoare_autoconsum = autoconsum_total * pret_autoconsum
valoare_injectare = injectie_retea * pret_injectare
cost_energie_retea = consum_retea * pret_retea
venit_total = valoare_autoconsum + valoare_injectare

investitie_pv = putere_pv * 1000 * cost_pv_kwp
investitie_baterie = capacitate_baterie * 1000 * cost_baterie_kwh
investitie_totala = investitie_pv + investitie_baterie

OandM = investitie_totala * 0.015
economie_neta = venit_total - OandM - cost_energie_retea
payback = investitie_totala / economie_neta if economie_neta > 0 else float('inf')

# Rezultate
st.write("### Rezultate detaliate:")
st.write(f"- Consum anual total: {consum_anual:.0f} MWh")
st.write(f"- Autoconsum total: {autoconsum_total:.0f} MWh")
st.write(f"- Energie injectată în rețea: {injectie_retea:.0f} MWh")
st.write(f"- Consum din rețea: {consum_retea:.0f} MWh")
st.write(f"- Valoare autoconsum: {valoare_autoconsum:.0f} €")
st.write(f"- Valoare energie injectată: {valoare_injectare:.0f} €")
st.write(f"- Cost energie din rețea: {cost_energie_retea:.0f} €")
st.write(f"- Venit total: {venit_total:.0f} €")
st.write(f"- Investiție totală: {investitie_totala:.0f} €")
st.write(f"- Costuri O&M anuale: {OandM:.0f} €")
st.write(f"- Economie netă anuală: {economie_neta:.0f} €")
st.write(f"- Payback: {payback:.2f} ani")

# Grafic
labels = ['Autoconsum (MWh)', 'Injectare (MWh)', 'Rețea (MWh)', 'Venit total (k€)', 'Economie netă (k€)', 'Payback (ani)']
values = [autoconsum_total, injectie_retea, consum_retea, venit_total / 1000, economie_neta / 1000, payback]

fig, ax = plt.subplots()
ax.bar(labels, values, color='skyblue')
ax.set_ylabel('Valori')
ax.set_title('Rezultate economice detaliate (cu profil orar)')
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)
