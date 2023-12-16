    // lấy checkin time
    const CheckInTime = await getLatestCheckInTime(id);
    console.log(CheckInTime);
    // const currentTime = formattedTime;  
    // lấy tg hiện tại
    const currentTimeParsed = parseISO(formattedTime, 'yyyy-MM-dd HH:mm:ss', new Date());
    console.log(currentTimeParsed);
    // lấy tg chênh lệch
    const hoursDifference = differenceInHours(currentTimeParsed, CheckInTime);
    console.log(hoursDifference);
    if(true) {
      // update bảng history
      const updateHistoryQuery = `UPDATE history SET TimeCheckOut = '${formattedTime}', Cash = ${(hoursDifference == 0) ? 10000 : hoursDifference* 1000} WHERE IdCard = ${id} AND TimeCheckOut IS NULL`;

      mysqlConnection.query(updateHistoryQuery, (err, result) => {
        if (err) {
          console.error('Error updating data in history table:', err);
        } else {
          if (result.affectedRows > 0) {
            console.log('Data updated in history table successfully.');
            // Thực hiện các hành động khác nếu cần
          } else {
            console.log('No matching record found to update.');
          }
        }
      });

      //update bảng card
      const updateCardQuery = `UPDATE card SET IsCheckIn = 0 WHERE ID = ${id}`;

      mysqlConnection.query(updateCardQuery, (err, result) => {
        if (err) {
          console.error('Error updating data in card table:', err);
        } else {
          if (result.affectedRows > 0) {
            console.log('Data updated in card table successfully.');
            // Thực hiện các hành động khác nếu cần
          } else {
            console.log('No matching record found to update.');
          }
        }
      });
    }