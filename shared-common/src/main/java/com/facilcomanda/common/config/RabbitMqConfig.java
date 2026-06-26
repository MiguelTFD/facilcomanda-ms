package com.facilcomanda.common.config;
import com.facilcomanda.common.event.EventPublisher;
import org.springframework.amqp.core.*;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
@Configuration
public class RabbitMqConfig {
    @Bean TopicExchange domainExchange() { return ExchangeBuilder.topicExchange(EventPublisher.DOMAIN_EXCHANGE).durable(true).build(); }
    @Bean TopicExchange auditExchange() { return ExchangeBuilder.topicExchange(EventPublisher.AUDIT_EXCHANGE).durable(true).build(); }
    @Bean Queue auditQueue() { return QueueBuilder.durable("audit.queue").withArgument("x-dead-letter-exchange", "audit.events.dlx").build(); }
    @Bean TopicExchange auditDlx() { return ExchangeBuilder.topicExchange("audit.events.dlx").durable(true).build(); }
    @Bean Binding auditBinding(Queue auditQueue, TopicExchange auditExchange) { return BindingBuilder.bind(auditQueue).to(auditExchange).with("audit.created"); }
    @Bean MessageConverter jsonMessageConverter() { return new Jackson2JsonMessageConverter(); }
}
