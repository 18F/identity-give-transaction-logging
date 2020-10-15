package gov.gsa.give.transaction.logs.model;

import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import javax.persistence.*;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;
import java.io.Serializable;
import java.sql.Timestamp;
import java.time.ZonedDateTime;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name="transaction_log")
public class TransactionLog implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long logid; //transaction log id
    //@Column(unique = true) to do: make rpid unique
    private String rpid; //relying party id for login it would be uuid


    @Column(updatable=false)
    @CreationTimestamp
    private Timestamp created_date;
    @Column
    @UpdateTimestamp
    private Timestamp modified_date;
    //private ZonedDateTime start_time;
    //private ZonedDateTime end_time;
    //private ZonedDateTime transaction_time;
    private String proofing_status;
    private String proofing_result;
    private String vendor;
}








