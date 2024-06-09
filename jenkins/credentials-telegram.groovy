import java.io.File
import groovy.xml.XmlUtil
import groovy.xml.*
import hudson.model.*

// Функція для отримання змінних середовища
def getEnvVariable(String name) {
    return System.getenv(name)
}

def newtelegramBotToken = getEnvVariable('TELEGRAM_JENKINS_BOT_TOKEN')
def newtelegramBotName = getEnvVariable('TELEGRAM_JENKINS_BOT_NAME')

// Налаштування плагіну Telegram Bot
def jenkinsHome = "/var/jenkins_home"
def telegramConfigFile = ""
try{
    telegramConfigFile = new File(jenkinsHome, "jenkinsci.plugins.telegrambot.TelegramBotGlobalConfiguration.xml")
    def xml = new XmlSlurper().parse(telegramConfigFile)
    
    // Читання поточних значень
    if((xml.botToken == newtelegramBotToken) || (xml.botName == newtelegramBotName)){
        println "no change"
    }
    else{
        println "change"
    }
    
    xml.botToken.replaceNode { botToken(newtelegramBotToken) }
    xml.botName.replaceNode { botName(newtelegramBotName) }
    
    // Збереження змін
    def writer = new StringWriter()
    XmlUtil.serialize(xml, writer)
    
    telegramConfigFile.text = writer.toString()
    
    
}catch(FileNotFoundException ex) {
    println "Configuration file not found, creating a new one!"
    
    // Створення нової конфігурації
    def xmlContent = """
    <jenkinsci.plugins.telegrambot.TelegramBotGlobalConfiguration plugin="telegram-notifications@1.4.0">
        <botToken>${newtelegramBotToken}</botToken>
        <botName>${newtelegramBotName}</botName>
        <approvalType>ALL</approvalType>
    </jenkinsci.plugins.telegrambot.TelegramBotGlobalConfiguration>
    """
    println "New configuration file created with Bot Token:  and Chat ID: "
    telegramConfigFile.text = xmlContent
}
