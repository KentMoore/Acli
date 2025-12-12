package filter;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.filter.TimestampsFilter;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;

public class TimeStampFilterDemo {
    static Connection connection;
    static Table table;
    public static void main(String[] args) throws IOException {
        connection= HBaseConnect.getConnection();
        TableName tableName=TableName.valueOf("commodity1:fruit_table");
        table=connection.getTable(tableName);
        //创建Scan对象
        Scan scan=new Scan();
        //创建时间戳过滤器，只有一个参数，长整型List,List<Long>,返回：包含该时间戳的单元格
        TimestampsFilter timestampsFilter=new TimestampsFilter(Arrays.asList(1764746171256L));
        //将过滤器配置到scan对象
        scan.setFilter(timestampsFilter);
        //table调用getScanner()方法查询数据，遍历打印查询结果
        for(Result result:table.getScanner(scan)){
            List<Cell> cellList=result.listCells();
            for(Cell cell:cellList){
                String rowKey=new String(
                        cell.getRowArray(),
                        cell.getRowOffset(),
                        cell.getRowLength()
                );
                System.out.println("水果编号："+rowKey);
            }
        }
        HBaseConnect.closeConnection();
    }
}