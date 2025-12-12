package namespace;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.NamespaceDescriptor;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;

import java.io.IOException;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

public class GetNamespaceDesc {
    public static void main(String[] args) throws IOException {
        Connection conn= HBaseConnect.getConnection();
        Admin admin= conn.getAdmin();
        NamespaceDescriptor empolyee=admin.getNamespaceDescriptor("commodity1");
        Map<String,String> empolyeeConfiguration=empolyee.getConfiguration();
        Set<String> keys=empolyeeConfiguration.keySet();
        Iterator<String> keyIterator= keys.iterator();
        while(keyIterator.hasNext()){
            String key=keyIterator.next();
            String value=empolyeeConfiguration.get(key);
            System.out.println("属性："+key+"\t属性值："+value);
        }
        HBaseConnect.closeConnection();
    }
}
