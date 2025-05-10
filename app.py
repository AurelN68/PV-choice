import streamlit as st

st.title("Analiză Economică PV + Storage")

# Input utilizator
consum = st.slider('Consum fabrică (MWh/an)', 0.1, 20.0, 1.4)
consum = consum * 1000  # conversie la MWh/an
putere_pv = st.slider('Putere PV (MWp)', 0.5, 5.0, 2.0)
capacitate_baterie = st.slider('Capacitate baterie (kWh)', 0, 10000, 2000)

# Calcule economice
cost_pv_kwp = 800
cost_baterie_kwh = 400
pret_autoconsum = 160
pret_injectare = 55
ore_pv = 1200

energie_pv = putere_pv * ore_pv
autoconsum = min(consum, energie_pv)
injectie = max(energie_pv - consum, 0)

valoare_autoconsum = autoconsum * pret_autoconsum
valoare_injectare = injectie * pret_injectare
venit_total = valoare_autoconsum + valoare_injectare

investitie_pv = putere_pv * 1000 * cost_pv_kwp
investitie_baterie = capacitate_baterie * cost_baterie_kwh
investitie_totala = investitie_pv + investitie_baterie

OandM = investitie_totala * 0.015
economie_neta = venit_total - OandM
payback = investitie_totala / economie_neta

# Rezultate
st.write("### Rezultate detaliate:")
st.write(f"- Autoconsum: {autoconsum:.0f} MWh")
st.write(f"- Energie injectată: {injectie:.0f} MWh")
st.write(f"- Venit total: {venit_total:.0f} €")
st.write(f"- Investiție totală: {investitie_totala:.0f} €")
st.write(f"- Costuri O&M anuale: {OandM:.0f} €")
st.write(f"- Economie netă anuală: {economie_neta:.0f} €")
st.write(f"- Payback: {payback:.2f} ani")
import matplotlib.pyplot as plt

labels = ['Autoconsum', 'Injectare', 'Venit total (k€)', 'Economie netă (k€)', 'Payback (ani)']
values = [autoconsum, injectie, venit_total / 1000, economie_neta / 1000, payback]

fig, ax = plt.subplots()
bars = ax.bar(labels, values)
ax.set_ylabel('Valoare')
ax.set_title('Rezultate economice')
st.pyplot(fig)
