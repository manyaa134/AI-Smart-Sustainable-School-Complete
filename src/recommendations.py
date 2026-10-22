def recommendations(predictions,statuses,context):
    result=[];opened=bool(context.get("school_open",1));event=bool(context.get("is_school_event",0))
    rules={"water_consumption_litres":("Water","Review meter readings, inspect for leaks, and check irrigation and cleaning schedules."),"electricity_consumption_kwh":("Electricity","Review lighting, cooling and equipment schedules; check unused areas."),"waste_generation_kg":("Waste","Review segregation, reusable items, recycling collection and bin placement.")}
    for t,(label,action) in rules.items():
        s=statuses.get(t,"UNAVAILABLE")
        if s=="UNAVAILABLE":continue
        if not opened and s=="LOW":result.append((label,"Context check","School is marked closed. Verify meter readings and closure dates."))
        elif s=="HIGH":
            if event:action += " Since an event is planned, review event-related facilities and waste."
            result.append((label,"Review recommended",action))
        elif s=="LOW":result.append((label,"Verify context","Check reading completeness, operating status and attendance. Low use is not always good."))
        else:result.append((label,"Routine monitoring","Compare with similar school days and continue monitoring."))
    return result
