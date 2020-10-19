package gov.gsa.give.transaction.logs.controller;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.validation.Valid;

import gov.gsa.give.transaction.logs.model.TransactionLog;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


import gov.gsa.give.transaction.logs.exception.ResourceNotFoundException;
import gov.gsa.give.transaction.logs.service.TransactionLoggingService;

@RestController
@RequestMapping("/api/v1")
public class TransactionLoggingController {


    @Autowired
    private TransactionLoggingService loggingService;


    //Creates a new transaction log
    @PostMapping("/transaction")
    public TransactionLog createNewTransaction(@RequestBody TransactionLog transaction) {
        return loggingService.createTransaction(transaction);

    }
    //Returns all transactions
    @GetMapping("/transaction")
    public List<TransactionLog> getAllTransactions(){
        return loggingService.getTransactionLogs();
    }

    //Returns all transactions with specified rpid
    @GetMapping("/transaction/{rpid}")
    public ResponseEntity<List<TransactionLog>> getTransactionByRpid(@PathVariable(value = "rpid") String rpid) {
        List<TransactionLog> transactionsByRpid = loggingService.getTransactionLogByRpid(rpid);
        /*If we don't want to return a 200 with empty list, edit this if statement
        /*
        if (transactionsByRpid.isEmpty()){
             return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }*/
        return ResponseEntity.ok().body(transactionsByRpid);
    }
    //Returns specific log by logid
    @GetMapping("/transaction/logs/{logid}")
    public ResponseEntity<TransactionLog> getTransactionById(@PathVariable(value = "logid") Long logid) throws ResourceNotFoundException {
        TransactionLog transaction = loggingService.getTransactionLogByLogid(logid).orElseThrow(() -> new ResourceNotFoundException("Log not found for:: " + logid));
        return ResponseEntity.ok().body(transaction);
    }


    //Updates transaction based on logid
    @PutMapping("/transaction/{logid}")
    public ResponseEntity<TransactionLog> updateTransaction(@PathVariable(value = "logid") Long logid,
                                                   @Valid @RequestBody TransactionLog transactionDetails) throws ResourceNotFoundException {
        TransactionLog transaction = loggingService.getTransactionLogByLogid(logid).orElseThrow(() -> new ResourceNotFoundException("Log not found for:: " + logid));

        TransactionLog updatedTransaction = loggingService.updateTransactionLog(transaction, transactionDetails);

        return ResponseEntity.ok(updatedTransaction);
    }

    @DeleteMapping("/transaction/{logid}")
    public Map<String, Boolean> deleteTransaction(@PathVariable(value = "logid") Long logid)
            throws ResourceNotFoundException {
        TransactionLog transaction = loggingService.getTransactionLogByLogid(logid).orElseThrow(() -> new ResourceNotFoundException("Log not found for:: " + logid));
        loggingService.deleteTransactionLog(transaction);
        Map<String, Boolean> response = new HashMap<>();
        response.put("deleted", Boolean.TRUE);
        return response;
    }

}