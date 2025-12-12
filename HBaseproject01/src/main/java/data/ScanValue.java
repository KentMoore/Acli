package data;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;
import java.util.List;

public class ScanValue {
    public static void main(String[] args) throws IOException {
        //1.获取连接
        Connection connection = HBaseConnect.getConnection();
        //2.获取表对象
        TableName tableName = TableName.valueOf("commodity1:fruit_table");
        Table table = connection.getTable(tableName);
        // 3.构造Scan对象
        Scan scan = new Scan();
        // 4.table调用getScanner()查询数据，返回ResultScanner
        ResultScanner results = table.getScanner(scan);
        for (Result result : results){
            showResult(result);
        }
        // 5.关闭连接
        HBaseConnect.closeConnection();
    }

    public static void showResult(Result result) {
        List<Cell> cellList = result.listCells();

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

            // ============ 修改：根据列名判断类型 ============
            String value;
            if (qualifier.equals("quantity")) {
                // quantity 是 Long 类型，用 Bytes.toLong() 读取
                long longValue = Bytes.toLong(
                        cell.getValueArray(),
                        cell.getValueOffset()
                );
                value = String.valueOf(longValue);
            } else {
                // 其他字段是 String 类型
                value = new String(
                        cell.getValueArray(),
                        cell.getValueOffset(),
                        cell.getValueLength()
                );
            }

            System.out.println("行键：" + rowkey + "\t" +
                    "列族：" + columnFamily + "\t" +
                    "列名：" + qualifier + "\t" +
                    "值：" + value + "\t" +
                    "时间戳：" + timestamp);
        }
        System.out.println("----------------------------------------");
    }
}
