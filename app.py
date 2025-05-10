import streamlit as st
import matplotlib.pyplot as plt

st.title("Analiză Economică PV + Storage")

# Input utilizator
consum_orar = st.slider('Consum mediu orar al fabricii (MWh)', 0.0, 5.0, 1.0)
consum_anual = consum_orar * 24 * 365
putere_pv = st.slider('Putere PV (MWp)', 0.0, 15.0, 2.0)
capacitate_baterie = st.slider('Capacitate baterie (MWh)', 0.0, 100.0, 10.0)

# Calcule economice
cost_pv_kwp = 800
cost_baterie_kwh = 400
pret_autoconsum = 160
pret_injectare = 55
pret_retea = 160
ore_pv = 1200

energie_pv = putere_pv * ore_pv
autoconsum = min(consum_anual, energie_pv)
injectie = max(energie_pv - consum_anual, 0)
consum_retea = max(consum_anual - energie_pv, 0)

valoare_autoconsum = autoconsum * pret_autoconsum
valoare_injectare = injectie * pret_injectare
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
st.write(f"- Autoconsum: {autoconsum:.0f} MWh")
st.write(f"- Energie injectată în rețea: {injectie:.0f} MWh")
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
values = [autoconsum, injectie, consum_retea, venit_total / 1000, economie_neta / 1000, payback]

fig, ax = plt.subplots()
ax.bar(labels, values, color='skyblue')
ax.set_ylabel('Valori')
ax.set_title('Rezultate economice detaliate')
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)
