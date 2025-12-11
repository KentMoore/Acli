package data;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Delete;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;

public class DeleteValue {
    public static void main(String[] args) throws IOException {
        Connection connection = HBaseConnect.getConnection();
        TableName tableName = TableName.valueOf("employee:staff_info");
        Table table = connection.getTable(tableName);
        Delete deleteRow = new Delete((Bytes.toBytes("staff0001")));
        deleteRow.addFamily(Bytes.toBytes("sale_info"));
        deleteRow.addColumn(Bytes.toBytes("delvelopment_info"),Bytes.toBytes("staff_info"));
        table.delete(deleteRow);
        HBaseConnect.closeConnection();
    }
}
