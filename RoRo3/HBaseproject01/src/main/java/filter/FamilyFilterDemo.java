package filter;

//import com.fspt.connect.HBaseConnect;
import connect.HBaseConnect;
import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.filter.BinaryComparator;
import org.apache.hadoop.hbase.filter.FamilyFilter;
import org.apache.hadoop.hbase.filter.RowFilter;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;
import java.math.BigDecimal;

public class FamilyFilterDemo {
    static Connection connection;
    static Table table;
    public static void main(String[] args) throws IOException {
        connection= HBaseConnect.getConnection();
        TableName tableName=TableName.valueOf("commodity1:fruit_table");
        table=connection.getTable(tableName);
        //创建Scan对象
        Scan scan=new Scan();
        // 创建列族过滤器,2参数：比较关系、比较器，返回：满足条件的行数据
        FamilyFilter rowFilter=new FamilyFilter(
                CompareOperator.EQUAL,
                new BinaryComparator(Bytes.toBytes("fruit_info"))
        );
        //将过滤器配置到scan对象
        scan.setFilter(rowFilter);
        //table调用getScanner()查询数据，并遍历打印结果
        for(Result result:table.getScanner(scan)){
            String fruitName=new String(result.getValue(Bytes.toBytes("fruit_info"),Bytes.toBytes("fruitName")));
            String fruitOrigin=new String(result.getValue(Bytes.toBytes("fruit_info"),Bytes.toBytes("fruitOrigin")));
            String fruitType=new String(result.getValue(Bytes.toBytes("fruit_info"),Bytes.toBytes("fruitType")));
            //获取rowKey（水果编号）的值
            String rowKey=new String(result.getRow());
            System.out.println("水果编号："+rowKey+",水果名："+fruitName+",水果类型："+fruitType+"，水果产地："+fruitOrigin);
        }
        HBaseConnect.closeConnection();
    }
}