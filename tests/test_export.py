def test_export_docx(client):
    # Deep-dive intake
    payload = {"answers":{"propertyType":"SFR","beds":3,"baths":2.0,"interiorSizeSqft":1800,"conditionBand":"updated",
                          "tightRooms":False,"naturalLight":"good","occupancy":"occupied","quirkyFlow":False,"signatureFeature":"Corner lot",
                          "likelyBuyer":"move_up","locationPerk":"parks","timelinePressure":"medium","agentOnCamComfort":"low","showingWindow":"evening"}}
    r = client.post("/intake/deep-dive", json=payload)
    iid = r.json()["intake_id"]
    r2 = client.post("/export/docx", json={"intake_id":iid,"chosen_tier":"High","chosen_bias_key":"fluency"})
    assert r2.status_code==200
    assert r2.json()["downloadUrl"].endswith(".docx")
