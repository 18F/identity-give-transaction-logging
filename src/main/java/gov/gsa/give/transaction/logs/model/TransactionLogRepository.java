package gov.gsa.give.transaction.logs.model;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TransactionLogRepository extends JpaRepository<TransactionLog, Long> {

    List<TransactionLog> findByRpid(String rpid);
    //Implement below once rpid is unique
    //TransactionLog findByRpid(String rpid);

}