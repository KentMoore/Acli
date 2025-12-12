package filter;

import java.io.IOException;
import java.util.List;

import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CellUtil;
import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.filter.BinaryComparator;
import org.apache.hadoop.hbase.filter.ValueFilter;
import org.apache.hadoop.hbase.util.Bytes;

import connect.HBaseConnect;

public class ValueFilterDemo02 {
    public static void main(String[] args) throws IOException {
        Connection connection = HBaseConnect.getConnection();
        TableName tableName = TableName.valueOf("commodity1:fruit_table");

        Table table = connection.getTable(tableName);

        Scan scan = new Scan();

        ValueFilter valueFilter = new ValueFilter(
            CompareOperator.EQUAL,
            new BinaryComparator(Bytes.toBytes("Stone fruits"))   
        );
        scan.setFilter(valueFilter);

        ResultScanner scanner = table.getScanner(scan);
        
        for (Result result : scanner) {
            List<Cell> cellList = result.listCells();
            for (Cell cell : cellList) {
                String rowkey = new String(
                    cell.getRowArray(),
                    cell.getRowOffset(),
                    cell.getRowLength()  
                );
                 System.out.println("行键: " + rowkey);
            }    
        }
        
        scanner.close();
        table.close();
        HBaseConnect.closeConnection();
    }
}