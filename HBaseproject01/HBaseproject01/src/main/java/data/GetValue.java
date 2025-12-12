package data;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Table;

import java.io.IOException;
import java.util.List;

public class GetValue {
    public static void main(String[] args) throws IOException {
        // 1.获取连接
        Connection connection = HBaseConnect.getConnection();
        // 2.获取table对象
        TableName tableName = TableName.valueOf("employee:staff1");
        Table table = connection.getTable(tableName);
        // 3.构造一个Get对象
        Get get = new Get("staff001".getBytes());
        get.addColumn("sale_info".getBytes(),"staff_name".getBytes());
        // 4.table调用get()方法查询数据，返回Result
        Result result = table.get(get);
//        showResult(result);

        // 添加：调用showResult方法显示查询结果
        if (result != null && !result.isEmpty()) {
            showResult(result);
        } else {
            System.out.println("未查询到数据！");
        }

        // 5.关闭连接
        table.close();
        HBaseConnect.closeConnection();
    }

    public static void showResult(Result result) {
        List<Cell> cellList = result.listCells();

        // 添加空值检查
        if (cellList == null || cellList.isEmpty()) {
            System.out.println("查询结果为空");
            return;
        }

        for (Cell cell : cellList) {
            String rowkey = new String(
                    cell.getRowArray(),
                    cell.getRowOffset(),
                    cell.getRowLength()
            );
            String columnFamily = new String(
                    cell.getFamilyArray(),
                    cell.getFamilyOffset(),
                    cell.getFamilyLength()
            );
            String qualifier = new String(
                    cell.getQualifierArray(),
                    cell.getQualifierOffset(),
                    cell.getQualifierLength()
            );
            long timestamp = cell.getTimestamp();
            String value = new String(
                    cell.getValueArray(),
                    cell.getValueOffset(),
                    cell.getValueLength()
            );
            System.out.println("行键：" + rowkey + "\t" +
                    "列族：" + columnFamily + "\t" +
                    "列名：" + qualifier + "\t" +
                    "值：" + value + "\t" +
                    "时间戳：" + timestamp);
        }
    }
}