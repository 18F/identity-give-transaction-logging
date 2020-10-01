package gov.gsa.give.transaction.logs.service;

import java.time.Duration;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import javax.annotation.PostConstruct;


import gov.gsa.give.transaction.logs.model.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.ExchangeStrategies;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.beans.factory.annotation.Autowired;
import reactor.core.publisher.Mono;

@Service
public class TransactionLoggingService {

    @Autowired
    private TransactionLogRepository transactionRepo;

    public TransactionLog createTransaction(TransactionLog transaction) {
        return transactionRepo.save(transaction);
    }

    public List<TransactionLog> getTransactionLogs() {
        return transactionRepo.findAll();
    }

    public List<TransactionLog> getTransactionLogByRpid(String rpid){
        //List<TransactionLog> transactionsByRpid =  transactionRepo.findByRpid(rpid);
        return transactionRepo.findByRpid(rpid);

    }
    public TransactionLog updateTransactionLog(TransactionLog transaction, TransactionLog transactionDetails) {

        //return transactionRepo.save(transaction);
        transaction.setRpid(transactionDetails.getRpid());
        transaction.setProofing_status(transactionDetails.getProofing_status());
        transaction.setProofing_result(transactionDetails.getProofing_result());
        transaction.setVendor(transactionDetails.getVendor());

        final TransactionLog updatedTransaction = transactionRepo.save(transaction);
        return updatedTransaction;


    }

    public Optional<TransactionLog> getTransactionLogByLogid(Long logid){
        return transactionRepo.findById(logid);
    }





}
