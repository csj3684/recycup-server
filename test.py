from datetime import datetime

thisMonth = datetime.now().month
targetDuration = 2
targetMonth = (thisMonth + 12 - targetDuration ) % 12
print(targetMonth)

db.cursor.execute(" \
        select totalSales.headName as headName, sum(salesAmount - coalesce(returnAmount, 0)) as depositToBeReturned \
        from ( \
            (select phoneNumber, headName, sum(amount) as salesAmount \
            from recycup.sales \
            where month(date) = targetMonth\
            group by phoneNumber, headName)totalSales \
            left outer join \
            (select phoneNumber, headName, sum(amount) as returnAmount \
            from recycup.recycle \
            where month(date) = targetMonth\
            group by phoneNumber, headName)totalReturn \
            on totalSales.phoneNumber = totalReturn.phoneNumber and totalSales.headName = totalReturn.headName \
            ) \
        group by headName \
        ")