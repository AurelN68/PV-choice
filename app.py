import streamlit as st
import matplotlib.pyplot as plt

st.title("Analiză Economică PV + Storage")

# Input utilizator
consum = st.slider('Consum anual fabrică (MWh/an)', 0, 20000, 14000)
putere_pv = st.slider('Capacitate parc PV (MWh/an)', 0, 50000, 24000)
capacitate_baterie = st.slider('Capacitate stocare (MWh)', 0, 100, 20)

# Parametri economici standard
cost_pv_kwp = 800  # €/kWp
cost_baterie_kwh = 400  # €/kWh
pret_autoconsum = 160  # €/MWh
pret_injectare = 55  # €/MWh
OandM_percent = 1.5  # % pe an

# Calculul energiei disponibile din PV și consum
energie_pv_produsa = putere_pv
energie_autoconsumata = min(consum, energie_pv_produsa)
energie_injectata = max(energie_pv_produsa - consum, 0)

# Valori economice
valoare_autoconsum = energie_autoconsumata * pret_autoconsum
valoare_injectare = energie_injectata * pret_injectare
venit_total = valoare_autoconsum + valoare_injectare

# Costuri investiție
investitie_pv = (putere_pv / 1200) * 1000 * cost_pv_kwp  # estimăm 1200 kWh/kWp/an
investitie_baterie = capacitate_baterie * 1000 * cost_baterie_kwh
investitie_totala = investitie_pv + investitie_baterie

# Costuri operare
cost_OandM = investitie_totala * OandM_percent / 100

# Economie și Payback
economie_neta = venit_total - cost_OandM
payback = investitie_totala / economie_neta if economie_neta > 0 else float('inf')

# Rezultate textuale
st.write("### Rezultate detaliate:")
st.write(f"- Energie produsă PV: {energie_pv_produsa:.0f} MWh")
st.write(f"- Energie autoconsum: {energie_autoconsumata:.0f} MWh")
st.write(f"- Energie injectată: {energie_injectata:.0f} MWh")
st.write(f"- Valoare autoconsum: {valoare_autoconsum:.0f} €")
st.write(f"- Valoare injecție în rețea: {valoare_injectare:.0f} €")
st.write(f"- Venit total: {venit_total:.0f} €")
st.write(f"- Investiție totală: {investitie_totala:.0f} €")
st.write(f"- Cost operare anual: {cost_OandM:.0f} €")
st.write(f"- Economie netă anuală: {economie_neta:.0f} €")
st.write(f"- Payback: {payback:.2f} ani")

# Reprezentare grafică
labels = ['Autoconsum (MWh)', 'Injectare (MWh)', 'Venit total (k€)', 'Economie netă (k€)', 'Payback (ani)']
values = [energie_autoconsumata, energie_injectata, venit_total / 1000, economie_neta / 1000, payback]

fig, ax = plt.subplots()
bars = ax.bar(labels, values, color=['green', 'blue', 'orange', 'purple', 'red'])
ax.set_ylabel('Valoare')
ax.set_title('Rezultate economice')
ax.grid(True, axis='y', linestyle='--', alpha=0.7)

# Adăugăm valori pe bare
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

st.pyplot(fig)
